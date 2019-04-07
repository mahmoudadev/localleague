from django.contrib import admin
from .models import League, Round, Match, Standings, ParticipateInvite

admin.site.register(League)



class InlineMatch(admin.StackedInline):
    model = Match


class RoundAdmin(admin.ModelAdmin):
    inlines = [InlineMatch]



admin.site.register(Round, RoundAdmin)



admin.site.register(Match)


class StandingsAdmin(admin.ModelAdmin):
    list_display = ['league', 'match', 'team', 'points', 'wins', 'draws', 'losses']

admin.site.register(Standings, StandingsAdmin)

admin.site.register(ParticipateInvite)