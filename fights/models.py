from django.db import models


class Fighter(models.Model):

    name = models.CharField(max_length=255)
    birthday = models.CharField(max_length=255)
    dt_birthday = models.DateTimeField(null=True, blank=True)
    height = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    sh_url = models.CharField(max_length=255, unique=True)

    country = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    camp = models.CharField(max_length=255, null=True, blank=True)

    @property
    def fight_count(self):
        return self.winners.count() + self.losers.count()

    @property
    def decision_rate(self):
        decisions = self.winners.filter(
            method__icontains='Decision').count() + self.losers.filter(
            method__icontains='Decision'
        ).count()
        return decisions / self.fight_count

    @property
    def finish_rate(self):
        return 1 - self.decision_rate

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=255)
    organization = models.CharField(max_length=255)
    date_string = models.CharField(max_length=50)
    dt_date = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255)
    sh_url = models.CharField(max_length=255, null=True, blank=True,
                                   unique=True)

    def __str__(self):
        return self.title


class Fight(models.Model):
    winner = models.ForeignKey(Fighter, null=True, blank=True,
                               related_name='winners')
    winner_name = models.CharField(max_length=255)
    winner_url = models.CharField(max_length=255)

    loser = models.ForeignKey(Fighter, null=True, blank=True,
                              related_name='losers')
    loser_name = models.CharField(max_length=255)
    loser_url = models.CharField(max_length=255)

    event = models.ForeignKey(Event, null=True, blank=True)
    method = models.CharField(max_length=255)
    finish_type = models.CharField(max_length=50, null=True, blank=True)

    referee = models.CharField(max_length=255)
    round = models.CharField(max_length=255)
    time = models.CharField(max_length=255)

    def get_finish_type(self):
        finish_types = ['submission', 'ko', 'decision', 'draw', 'nc']
        method = self.method.lower()

        for finish in finish_types:
            if finish in method:
                return finish
        return None

    def calc_stats(self):
        pass

    class Meta:
        unique_together = ('winner', 'loser', 'event')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '{} defeated {}'.format(self.winner_name, self.loser_name)
