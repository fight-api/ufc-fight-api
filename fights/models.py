from django.db import models


class Fighter(models.Model):

    name = models.CharField(max_length=255)
    birthday = models.CharField(max_length=255)
    height = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    sherdog_url = models.CharField(max_length=255)

    country = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    camp = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Fight(models.Model):
    winner = models.ForeignKey(Fighter, null=True, blank=True,
                               related_name="winning")
    winner_name = models.CharField(max_length=255)
    winner_url = models.CharField(max_length=255)

    loser = models.ForeignKey(Fighter, null=True, blank=True,
                              related_name="losing")
    loser_name = models.CharField(max_length=255)
    loser_url = models.CharField(max_length=255)

    method = models.CharField(max_length=255)
    referee = models.CharField(max_length=255)
    round = models.CharField(max_length=255)
    time = models.CharField(max_length=255)

    def __str__(self):
        return "{} defeated {}".format(self.winner_name, self.loser_name)


# x={'loser_name': 'Urijah Faber',
#  'loser_url': '/fighter/Urijah-Faber-8847',
#  'method': 'Decision (Unanimous)',
#  'referee': 'Herb Dean',
#  'round': '5',
#  'time': '5:00',
#  'winner_name': 'Dominick Cruz',
#  'winner_url': '/fighter/Dominick-Cruz-12107'}
