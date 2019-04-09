from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.models import User, Player
from teams.models import PlayerInvite, TeamRequest, Team


def list(request):
    try:
        players = Player.objects.filter(is_teamleader=False)
        return render(request, 'players/list.html', {'players': players})
    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})


def player_profile(request, id):
    person = User.objects.get(id=id)
    return render(request, 'players/show.html', {'person': person })



def accept_invite(request, id):
    invite_request = PlayerInvite.objects.get(id=id)
    invite_request.checked = True
    invite_request.save()
    player = request.user.player
    team = invite_request.team
    team.players.add(player)
    team.save()
    return redirect('teams:show', team.id)


def reject_invite(request, id):
    invite_request = PlayerInvite.objects.get(id=id)
    invite_request.checked = True
    invite_request.save()
    return redirect('league:requests')



def team_request(request, id):
    try:
        team = Team.objects.get(id=id)
        TeamRequest.objects.create(player=request.user.player, team=team)
        return redirect('teams:list')
    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})
