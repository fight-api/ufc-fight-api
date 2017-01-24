from django.contrib import admin

from fights.models import Fighter, Fight, Event


@admin.register(Fighter)
class FighterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "birthday", "height", "weight", "nickname",
                    "location", "country", "camp", "sherdog_url")

    search_fields = ["sherdog_url", 'name']


@admin.register(Fight)
class FightAdmin(admin.ModelAdmin):
    list_display = ("id", "winner", "loser", "method", "round", "time",
                    "referee", 'event')

    search_fields = ["winner__name", 'loser__name', 'event__title']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Event._meta.fields]
