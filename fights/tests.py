from django.db import IntegrityError
from django.test import TestCase
import datetime

from fights.models import Fighter, Fight, Event, FightQuery


class FighterModelTests(TestCase):

    def setUp(self):
        self.fighter1 = Fighter.objects.create(
            name='f1',
            dt_birthday=datetime.datetime(1990, 1, 1),
            birthday='January 1st, 1990',
            height="5' 10",
            weight='170 lbs',
            sh_url='test.com/1'
        )
        self.fighter2 = Fighter.objects.create(
            name='f2',
            dt_birthday=datetime.datetime(1992, 6, 6),
            birthday='June 6th, 1992',
            height="5' 11",
            weight='170 lbs',
            sh_url='test.com/2'
        )
        self.event1 = Event.objects.create(
            title='event1',
            organization='org',
            date_string='Feb 2 2016',
            dt_date=datetime.datetime(2016, 2, 1),
            location='Las Vegas'
        )
        self.event2 = Event.objects.create(
            title='event2',
            organization='org',
            date_string='March 2 2016',
            dt_date=datetime.datetime(2016, 3, 1),
            location='Las Vegas'
        )
        self.event3 = Event.objects.create(
            title='event3',
            organization='org',
            date_string='April 2 2016',
            dt_date=datetime.datetime(2016, 4, 1),
            location='Las Vegas'
        )
        self.fight1 = Fight.objects.create(
            winner=self.fighter1,
            winner_name=self.fighter1.name,
            winner_url=self.fighter1.sh_url,
            loser=self.fighter2,
            loser_name=self.fighter2.name,
            loser_url=self.fighter2.sh_url,
            event=self.event1,
            method='ko',
            referee='Herb Dean',
            round='1',
            time='2.53'
        )
        self.fight2 = Fight.objects.create(
            winner=self.fighter1,
            winner_name=self.fighter1.name,
            winner_url=self.fighter1.sh_url,
            loser=self.fighter2,
            loser_name=self.fighter2.name,
            loser_url=self.fighter2.sh_url,
            event=self.event2,
            method='decision',
            referee='Herb Dean',
            round='3',
            time='5.00'
        )
        self.fight3 = Fight.objects.create(
            winner=self.fighter2,
            winner_name=self.fighter2.name,
            winner_url=self.fighter2.sh_url,
            loser=self.fighter1,
            loser_name=self.fighter1.name,
            loser_url=self.fighter1.sh_url,
            event=self.event3,
            method='submission',
            referee='Herb Dean',
            round='2',
            time='2.53'
        )

    def test_fights_on_date(self):
        before = datetime.datetime(2015, 1, 1)
        before_count = self.fighter1.fights_on_date(before)
        after = datetime.datetime(2017, 1, 1)
        after_count = self.fighter2.fights_on_date(after)
        one_fight_date = datetime.datetime(2016, 2, 15)
        one_count = self.fighter1.fights_on_date(one_fight_date)

        self.assertEqual(before_count, 0)
        self.assertEqual(after_count, 3)
        self.assertEqual(one_count, 1)

    def test_int_age_on_date(self):
        d1 = datetime.datetime(2016, 1, 2)
        d2 = datetime.datetime(2016, 5, 30)
        d3 = datetime.datetime(2016, 11, 30)
        d4 = datetime.datetime(1992, 7, 1)

        self.assertEqual(self.fighter1.age_on_date(d1)[1], 26)
        self.assertEqual(self.fighter1.age_on_date(d2)[1], 26)
        self.assertEqual(self.fighter1.age_on_date(d3)[1], 26)
        self.assertEqual(self.fighter1.age_on_date(d4)[1], 2)

        self.assertEqual(self.fighter2.age_on_date(d1)[1], 23)
        self.assertEqual(self.fighter2.age_on_date(d2)[1], 23)
        self.assertEqual(self.fighter2.age_on_date(d3)[1], 24)
        self.assertEqual(self.fighter2.age_on_date(d4)[1], 0)

    def test_fight_count(self):
        self.assertEqual(self.fighter1.fight_count, 3)
        self.assertEqual(self.fighter2.fight_count, 3)

    def test_decision_rate(self):
        self.assertEqual(self.fighter1.decision_rate, 1/3)
        self.assertEqual(self.fighter2.decision_rate, 1/3)

    def test_finish_rate(self):
        self.assertEqual(self.fighter1.finish_rate, 2/3)
        self.assertEqual(self.fighter2.finish_rate, 2/3)


class FightModelTests(TestCase):
    def setUp(self):
        self.fighter1 = Fighter.objects.create(
            name='f1',
            dt_birthday=datetime.datetime(1990, 1, 1),
            birthday='January 1st, 1990',
            height="5' 10",
            weight='170 lbs',
            sh_url='test.com/1'
        )
        self.fighter2 = Fighter.objects.create(
            name='f2',
            dt_birthday=datetime.datetime(1992, 6, 6),
            birthday='June 6th, 1992',
            height="5' 11",
            weight='170 lbs',
            sh_url='test.com/2'
        )
        self.event1 = Event.objects.create(
            title='event1',
            organization='org',
            date_string='Feb 2 2016',
            dt_date=datetime.datetime(2016, 2, 1),
            location='Las Vegas'
        )
        self.event2 = Event.objects.create(
            title='event2',
            organization='org',
            date_string='March 2 2016',
            dt_date=datetime.datetime(2016, 3, 1),
            location='Las Vegas'
        )
        self.event3 = Event.objects.create(
            title='event3',
            organization='org',
            date_string='April 2 2016',
            dt_date=datetime.datetime(2016, 4, 1),
            location='Las Vegas'
        )
        self.fight1 = Fight.objects.create(
            winner=self.fighter1,
            winner_name=self.fighter1.name,
            winner_url=self.fighter1.sh_url,
            loser=self.fighter2,
            loser_name=self.fighter2.name,
            loser_url=self.fighter2.sh_url,
            event=self.event1,
            method='technical ko',
            referee='Herb Dean',
            round='1',
            time='2.53'
        )
        self.fight2 = Fight.objects.create(
            winner=self.fighter1,
            winner_name=self.fighter1.name,
            winner_url=self.fighter1.sh_url,
            loser=self.fighter2,
            loser_name=self.fighter2.name,
            loser_url=self.fighter2.sh_url,
            event=self.event2,
            method='split decision',
            referee='Herb Dean',
            round='3',
            time='5.00'
        )
        self.fight3 = Fight.objects.create(
            winner=self.fighter2,
            winner_name=self.fighter2.name,
            winner_url=self.fighter2.sh_url,
            loser=self.fighter1,
            loser_name=self.fighter1.name,
            loser_url=self.fighter1.sh_url,
            event=self.event3,
            method='submission',
            referee='Herb Dean',
            round='2',
            time='2.53'
        )

    def test_get_finish_type(self):
        self.assertEqual(self.fight1.get_finish_type(), 'ko')
        self.assertEqual(self.fight2.get_finish_type(), 'decision')
        self.assertEqual(self.fight3.get_finish_type(), 'submission')

    def test_set_fighter_ages(self):
        self.assertEqual(self.fight1.winner_age, 26.101369863013698)
        self.assertEqual(self.fight1.winner_int_age, 26)
        self.assertEqual(self.fight1.loser_age, 23.671232876712327)
        self.assertEqual(self.fight1.loser_int_age, 23)

        # Assign new birthday to fighters and re-set ages
        self.fighter1.dt_birthday = datetime.datetime(1991, 1, 1)
        self.fighter2.dt_birthday = datetime.datetime(1988, 6, 6)
        self.fight1.set_fighter_ages()

        self.assertAlmostEqual(self.fight1.winner_age, 25.101369863013698, 2)
        self.assertEqual(self.fight1.winner_int_age, 25)
        self.assertAlmostEqual(self.fight1.loser_age, 27.671232876712327, 2)
        self.assertEqual(self.fight1.loser_int_age, 27)

    def test_get_streak(self):

        self.assertEqual(self.fight1.get_streak(self.fighter1), 0)
        self.assertEqual(self.fight1.get_streak(self.fighter2), 0)
        self.assertEqual(self.fight2.get_streak(self.fighter1), 1)
        self.assertEqual(self.fight2.get_streak(self.fighter2), -1)
        self.assertEqual(self.fight3.get_streak(self.fighter1), 2)
        self.assertEqual(self.fight3.get_streak(self.fighter2), -2)

    def test_calc_stats(self):
        # Set new values to get different results from initial save
        self.fight3.method = 'majority draw'
        self.fight3.event.dt_date = datetime.datetime(2001, 1, 1)
        self.fight3.winner.dt_birthday = datetime.datetime(1990, 1, 1)
        self.fight3.loser.dt_birthday = datetime.datetime(1991, 1, 1)
        self.fight3.calc_stats()

        self.assertEqual(self.fight3.finish_type, 'draw')
        self.assertEqual(self.fight3.winner_experience, 0)
        self.assertEqual(self.fight3.loser_experience, 0)
        self.assertEqual(self.fight3.winner_int_age, 11)
        self.assertEqual(self.fight3.loser_int_age, 10)
        self.assertEqual(self.fight3.winner_streak, 0)
        self.assertEqual(self.fight3.loser_streak, 0)

    def test_str(self):
        self.assertEqual(str(self.fight1), 'f1 defeated f2')

    def test_unique_together(self):
        # assert error for non-unique
        with self.assertRaises(IntegrityError):
            Fight.objects.create(winner=self.fighter1, loser=self.fighter2, event=self.event1)


class FightQueryModelTests(TestCase):
    def setUp(self):
        self.fighter1 = Fighter.objects.create(
            name='f1',
            dt_birthday=datetime.datetime(1990, 1, 1),
            birthday='January 1st, 1990',
            height="5' 10",
            weight='170 lbs',
            sh_url='test.com/1'
        )
        self.fighter2 = Fighter.objects.create(
            name='f2',
            dt_birthday=datetime.datetime(1992, 6, 6),
            birthday='June 6th, 1992',
            height="5' 11",
            weight='170 lbs',
            sh_url='test.com/2'
        )
        self.event1 = Event.objects.create(
            title='event1',
            organization='org',
            date_string='Feb 2 2016',
            dt_date=datetime.datetime(2016, 2, 1),
            location='Las Vegas'
        )
        self.event2 = Event.objects.create(
            title='event2',
            organization='org',
            date_string='March 2 2016',
            dt_date=datetime.datetime(2016, 3, 1),
            location='Las Vegas'
        )
        self.event3 = Event.objects.create(
            title='event3',
            organization='org',
            date_string='April 2 2016',
            dt_date=datetime.datetime(2016, 4, 1),
            location='Las Vegas'
        )
        self.fight1 = Fight.objects.create(
            winner=self.fighter1,
            winner_name=self.fighter1.name,
            winner_url=self.fighter1.sh_url,
            loser=self.fighter2,
            loser_name=self.fighter2.name,
            loser_url=self.fighter2.sh_url,
            event=self.event1,
            method='technical ko',
            referee='Herb Dean',
            round='1',
            time='2.53'
        )
        self.fight2 = Fight.objects.create(
            winner=self.fighter1,
            winner_name=self.fighter1.name,
            winner_url=self.fighter1.sh_url,
            loser=self.fighter2,
            loser_name=self.fighter2.name,
            loser_url=self.fighter2.sh_url,
            event=self.event2,
            method='split decision',
            referee='Herb Dean',
            round='3',
            time='5.00'
        )
        self.fight3 = Fight.objects.create(
            winner=self.fighter2,
            winner_name=self.fighter2.name,
            winner_url=self.fighter2.sh_url,
            loser=self.fighter1,
            loser_name=self.fighter1.name,
            loser_url=self.fighter1.sh_url,
            event=self.event3,
            method='submission',
            referee='Herb Dean',
            round='2',
            time='2.53'
        )

    def test_get_query_filters(self):
        self.fight_query1 = FightQuery(min_age=20, max_age=40)
        self.assertDictEqual(
            self.fight_query1.get_query_filters(),
            {'age__gte': 20, 'age__lte': 40})

        self.fight_query1.win_loss_streak = 1
        self.assertDictEqual(self.fight_query1.get_query_filters(),
                             {'age__gte': 20, 'age__lte': 40, 'streak': 1})

        self.fight_query1.min_experience = 1
        self.fight_query1.max_experience = 12

        self.assertDictEqual(self.fight_query1.get_query_filters(),
                             {'age__gte': 20, 'age__lte': 40, 'streak': 1, 'experience__gte': 1, 'experience__lte': 12})


    def test_get_wins_losses(self):
        # Test streak, age, experience
        ## Get wins and losses for each, can use age to get unbalanced results
        pass
