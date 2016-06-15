from django.contrib import admin

from fights.models import Fighter, Fight


@admin.register(Fighter)
class FighterAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Fight)
class FightAdmin(admin.ModelAdmin):
    list_display = ("id", "fighter", "opponent", "win", "date", "finish",
                    "location", "weight", "moneyline", "nationality")
