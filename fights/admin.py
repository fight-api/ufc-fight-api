from django.contrib import admin

from fights.models import Fighter, Fight


@admin.register(Fighter)
class FighterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "birthday", "height", "weight", "nickname",
                    "location", "country", "camp", "sherdog_url")

    search_fields = ["sherdog_url"]


@admin.register(Fight)
class FightAdmin(admin.ModelAdmin):
    list_display = ("id", "winner", "loser", "method", "round", "time",
                    "referee")
