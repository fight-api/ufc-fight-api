from django.db import models

"""
New plan, get all ufc fights and store profile page for each fighter.
Then scrape each profile page and create fighter objects.



"""

class Fighter(models.Model):
    # Later add bio data and overall meta stats
    name = models.CharField(max_length=255)

    @property
    def weights(self):
        bouts = self.fight_set.all()
        weight_classes = [x.weight for x in bouts]
        return set(weight_classes)

    def __str__(self):
        return self.name


class Fight(models.Model):
    fighter = models.ForeignKey(Fighter)
    opponent = models.CharField(max_length=255)
    win = models.BooleanField()
    date = models.DateField()

    finish = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)
    moneyline = models.CharField(max_length=10)

    nationality = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return "{} vs {}".format(self.fighter, self.opponent)


# TO DO
# Save processed df to csv file
# create fighters from unique list
# Load all of the fights

