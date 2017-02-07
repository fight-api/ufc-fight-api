from bs4 import BeautifulSoup
import requests
from fights.models import Fighter, Fight, Event
from dateutil import parser


class FighterHandler:
    def __init__(self):
        self.base_url = 'http://www.sherdog.com'

    def name_from_url(self, url):
        name_section = url.split('/')[-1]
        names = name_section.split('-')[:-1]
        return ' '.join(names)

    def scrape_fighter_page(self, url):
        obj = {}
        r = requests.get(self.base_url + url)
        soup = BeautifulSoup(r.content, 'html.parser')
        bio = soup.find('div', class_='module bio_fighter vcard')
        names = bio.find(itemprop='name').find_all('span')

        if names:
            obj['name'] = names[0].text
        else:
            obj['name'] = self.name_from_url(url)

        if len(names) > 1:
            obj['nickname'] = names[1].text

        obj['url'] = url
        obj['birthday'] = bio.find('span', itemprop='birthDate').text
        obj['height'] = bio.find('span', class_='item height').find(
            'strong').text
        obj['weight'] = bio.find('span', class_='item weight').find(
            'strong').text

        location = bio.find(
            'span', itemprop='addressLocality', class_='locality')
        if location:
            obj['location'] = location.text

        country = bio.find('strong', itemprop='nationality')
        if country:
            obj['country'] = country.text

        camp = bio.find('span', itemprop='memberOf')
        if camp:
            obj['camp'] = camp.find('span', itemprop='name').text

        return obj

    def create_fighter_from_dict(self, d):

        fighter = Fighter.objects.create(name=d['name'],
                                         birthday=d['birthday'],
                                         height=d['height'],
                                         weight=d['weight'],
                                         sh_url=d['url'],
                                         nickname=d.get('nickname'),
                                         location=d.get('location'),
                                         country=d.get('country'),
                                         camp=d.get('camp')
                                         )
        return fighter

    def add_fighter_from_url(self, url):
        '''
        Scrape data from a fighter page and load it into the database and
         create a Fighter object with it.
        '''
        data = self.scrape_fighter_page(url)
        return self.create_fighter_from_dict(data)

    def get_fighter(self, fighter_url):
        '''
        Retrieve fighter from database, creating it if necessary.
        '''
        fighter = Fighter.objects.filter(sh_url=fighter_url).first()
        if not fighter:
            fighter = self.add_fighter_from_url(fighter_url)
        return fighter


class FightHandler:
    def __init__(self):
        self.base_url = 'http://www.sherdog.com'
        self.fighter_handler = FighterHandler()

    def add_events_to_results(self, results, soup, url):
        # results is a list of fight dicts
        event = EventHandler.create_event(soup, url)
        for res in results:
            res['event'] = event
        return results

    def capture_sub_fights(self, fights):
        results = []
        for fight in fights:
            obj = {}
            fighters = fight.find_all('div', class_='fighter_result_data')
            obj['winner_name'] = fighters[0].find('span', itemprop='name').text
            obj['winner_url'] = fighters[0].find('a').get('href')
            obj['loser_name'] = fighters[1].find('span', itemprop='name').text
            obj['loser_url'] = fighters[1].find('a').get('href')

            tds = fight.find_all('td')
            obj['method'] = tds[4].text.split('\n')[0]
            obj['referee'] = tds[4].text.split('\n')[1]
            obj['round'] = tds[5].text
            obj['time'] = tds[6].text

            results.append(obj)
        return results

    def capture_headliner(self, headliner, resume):
        obj = {}
        winner = headliner.find('div', class_='fighter left_side').find_all(
            'a')
        obj['winner_name'] = winner[1].text
        obj['winner_url'] = winner[1].get('href')

        loser = headliner.find('div', class_='fighter right_side').find_all(
            'a')
        obj['loser_name'] = loser[1].text
        obj['loser_url'] = loser[1].get('href')

        tds = resume.find_all('td')
        obj['method'] = tds[1].text
        obj['referee'] = tds[2].text
        obj['round'] = tds[3].text
        obj['time'] = tds[4].text

        return obj

    def scrape_fights(self, url):
        '''
        Scrapes all fights from a Sherdog event url.
        Returns a list of fight dicts.
        '''
        r = requests.get(self.base_url + url)
        soup = BeautifulSoup(r.content, 'html.parser')
        sub_fights = soup.find_all('tr', itemprop='subEvent')
        headliner = soup.find('div', class_='fight')
        resume = soup.find('table', class_='resume')

        results = self.capture_sub_fights(sub_fights)
        results.append(self.capture_headliner(headliner, resume))

        results = self.add_events_to_results(results, soup, url)
        return results

    def create_fight_from_dict(self, d):
        winner = self.fighter_handler.get_fighter(d['winner_url'])
        loser = self.fighter_handler.get_fighter(d['loser_url'])

        fight = Fight.objects.filter(
            winner=winner,
            winner_name=d['winner_name'],
            winner_url=d['winner_url'],
            loser=loser,
            loser_name=d['loser_name'],
            loser_url=d['loser_url'],
            method=d['method'],
            round=d['round'],
            time=d['time'],
            referee=d['referee'],
            event=None
        ).first()
        if fight:
            fight.event = d['event']
            fight.save()
        else:
            Fight.objects.update_or_create(
                winner=winner,
                winner_name=d['winner_name'],
                winner_url=d['winner_url'],
                loser=loser,
                loser_name=d['loser_name'],
                loser_url=d['loser_url'],
                method=d['method'],
                round=d['round'],
                time=d['time'],
                referee=d['referee'],
                event=d['event']
            )

    def create_fights_from_event(self, url):
        '''
        Takes an event url. Scrapes all fights and adds them to the database.
        '''
        fight_dicts = self.scrape_fights(url)
        for fd in fight_dicts:
            self.create_fight_from_dict(fd)


class EventHandler:

    def __init__(self):
        self.base_url = 'http://www.sherdog.com'

    @staticmethod
    def date_string_to_datetime(d):
        return parser.parse(d)

    @staticmethod
    def event_in_db(url):
        return Event.objects.filter(sh_url=url).count() > 0

    @staticmethod
    def create_event(soup, url):

        items = soup.find_all('span', itemprop='name')
        title = items[0].text
        organization = items[1].text
        start_date = soup.find('meta', itemprop='startDate').text
        location = soup.find('span', itemprop='location').text
        event, created = Event.objects.update_or_create(
            title=title,
            organization=organization,
            date_string=start_date,
            location=location,
            sh_url=url)
        return event


class SherdogEvents:
    def __init__(self):
        self.event_overview_url = 'http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2'
        self.fight_handler = FightHandler()

    def recent_event_urls(self):
        '''
        Returns a list of all event urls found on a Sherdog overview page.
        '''

        r = requests.get(self.event_overview_url)
        soup = BeautifulSoup(r.content, 'html.parser')
        events = soup.find('div', id='recent_tab')
        urls = events.find_all('a')
        return [x.get('href') for x in urls]

    def scrape_events(self):
        '''
        Add all new fights and events to the database.
        '''
        event_urls = self.recent_event_urls()
        for url in event_urls:

            if not EventHandler.event_in_db(url):
                self.fight_handler.create_fights_from_event(url)
            else:
                break
        return 'All up to date'
