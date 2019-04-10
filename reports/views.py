from django.shortcuts import render, redirect
from collections import OrderedDict
from leagues.models import League
from teams.models import Team



def leagues_summary(request):

    leagues = League.objects.all()

    teams_data = {}

    teams = Team.objects.all()
    for team in teams:
        teams_data[team.name] = {'number_of_members': team.players.all().count(), 'wins': 0, 'points': 0}
        standings = team.standings_set.all()
        for standing in standings:
            teams_data[team.name]['wins']  += standing.wins
            teams_data[team.name]['points']  += standing.points

    od = OrderedDict(sorted(teams_data.items(), key=lambda x: x[1]['points'], reverse=True))



    leagues_data = {}

    for league in leagues:
        leagues_data[league.name] = {}
        teams = {}
        for team in league.teams.all():
            teams[team.name ] = team.standings_set.get(league=league)

        leagues_data[league.name] = teams


    print(leagues_data)


    return render(request, 'reports/summary.html', {'leagues': leagues, 'teams': od , 'leagues_teams': leagues_data })