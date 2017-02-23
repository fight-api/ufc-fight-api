from django.contrib import admin

from fights.models import Fighter, Fight, Event


@admin.register(Fighter)
class FighterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'birthday', 'dt_birthday', 'height', 'weight', 'nickname',
                    'location', 'country', 'camp', 'sh_url')

    search_fields = ['sh_url', 'name']


@admin.register(Fight)
class FightAdmin(admin.ModelAdmin):
    list_display = ('id', 'winner', 'loser', 'method', 'round', 'time',
                    'referee', 'event', 'winner_age', 'loser_age', 'winner_streak', 'loser_streak', 'event_date')

    search_fields = ['winner__name', 'loser__name', 'event__title']

    def event_date(self, obj):
        return obj.event.dt_date

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Event._meta.fields]
