from django import forms
from fights.models import FightQuery


class FighterQueryForm(forms.ModelForm):

    class Meta:
        model = FightQuery
        fields = ('win_loss_streak', 'min_age', 'max_age')
