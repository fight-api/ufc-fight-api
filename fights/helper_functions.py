"""
Functions to help with loading or parsing new data.
"""
from fights.models import Fight, Fighter

def test_func():
    return "testing"


def create_fight(row):

    #n = row['name']
    #fighter = Fighter.objects.get(name=n)
    #print(fighter)
    fighter = Fighter.objects.get(name=row['name'])

    Fight.objects.create(fighter=fighter,
                         opponent=row['opponent'],
                         win=row['wl'],
                         date=row['date'],
                         finish=row['finish'],
                         location=row['location'],
                         moneyline=row['moneyline'],
                         weight=row['weight'],
                         nationality=row['nationality'])

