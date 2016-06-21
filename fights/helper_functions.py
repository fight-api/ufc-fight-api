"""
Functions to help with loading or parsing new data.
"""
from fights.models import Fighter, Fight


def create_fighter_from_dict(d):

    Fighter.objects.create(name=d["name"],
                           birthday=d["birthday"],
                           height=d["height"],
                           weight=d["weight"],
                           sherdog_url=d["url"],

                           nickname=d.get("nickname"),
                           location=d.get("location"),
                           country=d.get("country"),
                           camp=d.get("camp")
                           )


def create_fight_from_dict(d):
    winner = Fighter.objects.filter(sherdog_url=d["winner_url"]).first()
    loser = Fighter.objects.filter(sherdog_url=d["loser_url"]).first()
    Fight.objects.create(
        winner=winner,
        winner_name=d["winner_name"],
        winner_url=d["winner_url"],
        loser=loser,
        loser_name=d["loser_name"],
        loser_url=d["loser_url"],
        method=d["method"],
        round=d["round"],
        time=d["time"],
        referee=d["referee"]
    )



# winner = models.ForeignKey(Fighter, null=True, blank=True,
#                            related_name="winning")
# winner_name = models.CharField(max_length=255)
# winner_url = models.CharField(max_length=255)
#
# loser = models.ForeignKey(Fighter, null=True, blank=True,
#                           related_name="losing")
# loser_name = models.CharField(max_length=255)
# loser_url = models.CharField(max_length=255)
#
# method = models.CharField(max_length=255)
# referee = models.CharField(max_length=255)
# round = models.CharField(max_length=255)
# time = models.CharField(max_length=255)
