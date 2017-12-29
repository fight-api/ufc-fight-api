from django.test import TestCase
import datetime

from fights.models import Fighter, Fight, Event, FightQuery


class FighterModelTests(TestCase):

    def setUp(self):
        fighter1 = Fighter.objects.create(
            name='f1',
            dt_birthday=datetime.datetime(1990, 1, 1),
            birthday='January 1st, 1990',
            height="5' 10",
            weight='170 lbs',
            sh_rul='test.com'
        )

    def test_fights_on_date(self):
        pass

    def test_age_on_date(self):
        pass

    def test_fight_count(self):
        pass

    def test_decision_rate(self):
        pass

    def test_finish_rate(self):
        pass

