from rest_framework import serializers

from fights.models import Fighter, Fight, Event


class FightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fight
        fields = ('id', 'winner_name', 'loser_name', 'method', 'finish_type', 'referee', 'round',
                  'time')


class WinningFightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fight
        fields = ('id', 'loser_name', 'method', 'referee', 'round', 'time')


class LosingFightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fight
        fields = ('id', 'winner_name', 'method', 'referee', 'round', 'time')


class FighterListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fighter
        fields = ('id', 'name')


class FighterSerializer(serializers.ModelSerializer):

    winners = WinningFightSerializer(many=True, read_only=True)
    losers = LosingFightSerializer(many=True, read_only=True)

    class Meta:
        model = Fighter
        fields = ('id', 'name', 'nickname', 'birthday', 'height', 'weight',
                  'location', 'country', 'camp', 'fight_count',
                  'decision_rate', 'finish_rate', 'winners', 'losers')


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'title', 'organization', 'date_string', 'location')
