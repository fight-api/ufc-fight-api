"""
A collection of functions for parsing data.
"""

from fights.models import Fighter

def set_fighter_dt_birthday():
    for fighter in Fighter.objects.all():
        try:
            fighter.dt_birthday = fighter.birthday
            fighter.save()
        except:
            print(fighter.id)













