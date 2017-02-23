"""
A collection of functions for parsing data.
"""

from fights.models import Fighter, Fight


def set_fighter_dt_birthday():
    for fighter in Fighter.objects.all():
        try:
            fighter.dt_birthday = fighter.birthday
            fighter.save()
        except:
            print(fighter.id)


def set_fight_ages():
    for fight in Fight.objects.all():
        fight.set_fighter_ages()
        fight.save()


def set_win_streaks():
    for fight in Fight.objects.all():
        fight.set_fighter_streaks()
        fight.save()








