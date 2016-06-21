from bs4 import BeautifulSoup
import requests
import json

from fights.helper_functions import create_fighter_from_dict, \
    create_fight_from_dict
from fights.models import Fighter

missed_events = [
    '/events/UFC-176-Aldo-vs-Mendes-2-37609',
    '/events/UFC-151-Jones-vs-Henderson-25809'
]
missed_fighter = [
    '/fighter/Noad-Lahat-35732',
    '/fighter/Mirsad-Bektic-59766'
]


def capture_sub_fights(fights):
    results = []
    for fight in fights:
        obj = {}
        fighters = fight.find_all("div", class_="fighter_result_data")
        obj["winner_name"] = fighters[0].find('span', itemprop="name").text
        obj["winner_url"] = fighters[0].find('a').get('href')
        obj["loser_name"] = fighters[1].find('span', itemprop="name").text
        obj["loser_url"] = fighters[1].find('a').get('href')

        tds = fight.find_all("td")
        obj["method"] = tds[4].text.split("\n")[0]
        obj["referee"] = tds[4].text.split("\n")[1]
        obj["round"] = tds[5].text
        obj["time"] = tds[6].text

        results.append(obj)
    return results


def capture_headliner(headliner, resume):
    obj = {}
    winner = headliner.find('div', class_="fighter left_side").find_all('a')
    obj["winner_name"] = winner[1].text
    obj["winner_url"] = winner[1].get('href')

    loser = headliner.find('div', class_="fighter right_side").find_all('a')
    obj["loser_name"] = loser[1].text
    obj["loser_url"] = loser[1].get('href')

    tds = resume.find_all("td")
    obj["method"] = tds[1].text
    obj["referee"] = tds[2].text
    obj["round"] = tds[3].text
    obj["time"] = tds[4].text

    return obj


def scrape_page(url):
    """
    Scrapes all fights from a Sherdog event url.
    Returns a list of fight dicts.
    """
    r = requests.get('http://www.sherdog.com' + url)
    soup = BeautifulSoup(r.content, "html.parser")
    sub_fights = soup.find_all('tr', itemprop="subEvent")
    headliner = soup.find("div", class_="fight")
    resume = soup.find('table', class_='resume')

    results = capture_sub_fights(sub_fights)
    results.append(capture_headliner(headliner, resume))
    return results


def scrape_multiple_pages(urls):
    """
    Call scrape_page() on a list of urls and return a single list off all
    fight dicts.
    """
    results = []
    for url in urls:
        try:
            page_results = scrape_page(url)
            results.extend(page_results)
        except:
            print(url)
    return results


def all_event_urls(url):
    """
    Returns a list of all event urls found on a Sherdog overview page.
    """

    # Note: will need to filter for date and already captured events when
    # this is set up as a schedule.

    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    events = soup.find("div", id="events_list")
    urls = events.find_all("a")
    return [x.get("href") for x in urls]


def save_reviews(results, mode):
    with open("fight_data/stored_fights.json", mode) as file:
        data = json.dumps(results)
        file.write(data)


def load_reviews():
    with open("fight_data/stored_fights.json", "r") as file:
        data = file.read()
        return json.loads(data)


def update_reviews(results):
    older = load_reviews()
    older.extend(results)
    save_reviews(older, "w")


def all_fighter_urls():
    loaded = load_reviews()
    winners = [x["winner_url"] for x in loaded]
    losers = [x["loser_url"] for x in loaded]
    return list(set(winners+losers))


def scrape_fighter_page(url):
    obj = {}
    r = requests.get("http://www.sherdog.com" + url)
    soup = BeautifulSoup(r.content)
    bio = soup.find('div', class_="module bio_fighter vcard")
    names = bio.find(itemprop="name").find_all("span")

    obj["name"] = names[0].text
    if len(names) > 1:
        obj["nickname"] = names[1].text

    obj["url"] = url
    obj["birthday"] = bio.find('span', itemprop="birthDate").text
    obj["height"] = bio.find('span', class_="item height").find("strong").text
    obj["weight"] = bio.find('span', class_="item weight").find("strong").text

    location = bio.find(
        'span', itemprop="addressLocality", class_="locality")
    if location:

        obj["location"] = location.text

    country = bio.find('strong', itemprop="nationality")
    if country:
        obj["country"] = country.text

    camp = bio.find('span', itemprop="memberOf")
    if camp:
        obj["camp"] = camp.find("span", itemprop="name").text

    return obj


def check_fighter_urls(dicts):
    """
    Takes a list of fight dicts and grabs the winner and loser urls. Then
    returns any that are not in the database.
    """

    winners = [x["winner_url"] for x in dicts]
    losers = [x["loser_url"] for x in dicts]
    urls = winners + losers

    missing = [
        url for url in urls
        if not Fighter.objects.filter(sherdog_url=url).first()
        ]
    return missing


def add_fighter_from_url(url):
    """
    Scrape data from a fighter page and load it into the database and create
    a Fighter object with it.
    """
    data = scrape_fighter_page(url)
    create_fighter_from_dict(data)


def scrape_event_page(url):
    """
    url is a Sherdog UFC event page. This function will add any fighters not
    already in the database and then load all new fights in.
    """

    fight_results = scrape_page(url)
    missing_fighter_urls = check_fighter_urls(fight_results)

    if missing_fighter_urls:
        [add_fighter_from_url(x) for x in missing_fighter_urls]

    [create_fight_from_dict(x) for x in fight_results]

    return "Database updated"







if __name__ == '__main__':

    events_url = "http://www.sherdog.com/organizations/Ultimate-Fighting-Championship-2"
    #all_events = all_event_urls(events_url)
    #current_urls = all_events[14:-1]


