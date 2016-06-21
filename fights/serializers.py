from rest_framework import serializers

from fights.models import Fighter, Fight


class FightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fight
        fields = ("winner_name", "loser_name", "method", "referee", "round",
                  "time")


class WinningFightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fight
        fields = ("loser_name", "method", "referee", "round", "time")


class LosingFightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fight
        fields = ("winner_name", "method", "referee", "round", "time")


class FighterSerializer(serializers.ModelSerializer):

    winners = WinningFightSerializer(many=True, read_only=True)
    losers = LosingFightSerializer(many=True, read_only=True)

    class Meta:
        model = Fighter
        fields = ("name", "nickname", "birthday", "height", "weight",
                  "location", "country", "camp", "fight_count",
                  "decision_rate", "finish_rate", "winners", "losers")
