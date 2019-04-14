from django.contrib import admin
from .models import League, Round, Match, Standings, ParticipateInvite



class LeagueAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        update_fields = []
        print(form.initial)
        print(form.cleaned_data)

        # True if something changed in model
        # Note that change is False at the very first time
        if change:
            if form.initial['name'] != form.cleaned_data['name']:
                update_fields.append('name')
            if form.initial['description'] != form.cleaned_data['description']:
                update_fields.append('description')
            if form.initial['starts_at'] != form.cleaned_data['starts_at']:
                update_fields.append('starts_at')
            if form.initial['fees_per_team'] != form.cleaned_data['fees_per_team']:
                update_fields.append('fees_per_team')
            if form.initial['sponsor'] != form.cleaned_data['sponsor'].id:
                update_fields.append('sponsor')
            try:
                winner = form.cleaned_data['winner'].id
            except:
                winner = None
            if form.initial['winner'] != winner:
                update_fields.append('winner')

            obj.save(update_fields=update_fields)
        else:
            obj.save()

admin.site.register(League, LeagueAdmin)


class InlineMatch(admin.StackedInline):
    model = Match


class RoundAdmin(admin.ModelAdmin):
    inlines = [InlineMatch]


admin.site.register(Round, RoundAdmin)


class MatchAdmin(admin.ModelAdmin):


    list_display = ['round', 'home', 'away', 'location', 'result']
    list_filter = ['round']





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
        else:
            obj.save()





admin.site.register(Match, MatchAdmin)


class StandingsAdmin(admin.ModelAdmin):
    list_display = ['league', 'team', 'games_played', 'wins', 'draws', 'losses', 'points']


admin.site.register(Standings, StandingsAdmin)

admin.site.register(ParticipateInvite)
