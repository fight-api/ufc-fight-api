from rest_framework import serializers

#from fights.models import Fighter, Fight

#
# class FighterSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Fighter
#         fields = ("id", "name", "weights")
#
#
# class FightSerializer(serializers.ModelSerializer):
#
#     fighter = FighterSerializer(read_only=True)
#
#     class Meta:
#         model = Fight
#         fields = "__all__"
