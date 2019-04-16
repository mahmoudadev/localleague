from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from core.models import User, Player
from django.conf import settings
from teams.models import PlayerInvite, TeamRequest, Team

@login_required
def list(request):
    try:
        players = Player.objects.filter(is_teamleader=False)
        return render(request, 'players/list.html', {'players': players})
    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})

@login_required
def player_profile(request, id):
    person = User.objects.get(id=id)
    return render(request, 'accounts/show.html', {'person': person })


@login_required
def accept_invite(request, id):
    invite_request = PlayerInvite.objects.get(id=id)
    invite_request.checked = True
    invite_request.save()
    player = request.user.player
    team = invite_request.team
    team.players.add(player)
    team.save()

    msg = f"Congrats!, {invite_request.player.user} has accepted your join request for {team.name}. you can try to send join requests to other players from here: http://localfootballleague.pythonanywhere.com/players/  \n Thank your for your time \n best wishes \n Local Football League"
    try:
        send_mail(
            'notify about your team request',
            msg,
            settings.EMAIL_HOST_USER,
            [invite_request.player.user.email],
            fail_silently=False,
        )

    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})


    return redirect('teams:show', team.id)

@login_required
def reject_invite(request, id):
    invite_request = PlayerInvite.objects.get(id=id)
    team = invite_request.team
    invite_request.checked = True
    invite_request.save()

    msg = f"unfortunately, {invite_request.player.user} has rejected your join request for {team.name}. you can try to send join requests to other players from here: http://localfootballleague.pythonanywhere.com/players/  \n Thank your for your time \n best wishes \n Local Football League"
    try:
        send_mail(
            'notify about your team request',
            msg,
            settings.EMAIL_HOST_USER,
            [invite_request.player.user.email],
            fail_silently=False,
        )

    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})


    return redirect('league:requests')


@login_required
def team_request(request, id):
    try:
        team = Team.objects.get(id=id)
        TeamRequest.objects.create(player=request.user.player, team=team)
        return redirect('teams:list')
    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})


def list_team_invite(request):
    requests = request.user.player.playerinvite_set.filter(checked=False)
    return render(request, 'requests/team_join_requests.html', {'requests': requests})
