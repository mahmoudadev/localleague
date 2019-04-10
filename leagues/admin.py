from django.contrib import admin
from .models import League, Round, Match, Standings, ParticipateInvite

admin.site.register(League)


class InlineMatch(admin.StackedInline):
    model = Match


class RoundAdmin(admin.ModelAdmin):
    inlines = [InlineMatch]


admin.site.register(Round, RoundAdmin)


class MatchAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        update_fields = []
        print(form.initial)
        print(form.cleaned_data)

        # True if something changed in model
        # Note that change is False at the very first time
        if change:
            if form.initial['location'] != form.cleaned_data['location'].id:
                update_fields.append('location')
            if form.initial['away_score'] != form.cleaned_data['away_score']:
                update_fields.append('away_score')
            if form.initial['home_score'] != form.cleaned_data['home_score']:
                update_fields.append('home_score')
            if form.initial['result'] != form.cleaned_data['result']:
                update_fields.append('result')
            if form.initial['date'] != form.cleaned_data['date']:
                update_fields.append('date')

        obj.save(update_fields=update_fields)


admin.site.register(Match, MatchAdmin)


class StandingsAdmin(admin.ModelAdmin):
    list_display = ['league', 'match', 'team', 'points', 'wins', 'draws', 'losses']


admin.site.register(Standings, StandingsAdmin)

admin.site.register(ParticipateInvite)
