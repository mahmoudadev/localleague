from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from core.models import Player
from .forms import TeamForm
from teams.models import Team, PlayerInvite, TeamRequest

@login_required
def list(request):
    teams = Team.objects.all()
    return render(request, 'teams/list.html', {'teams': teams})

@login_required
def create(request):
    print(request.POST)
    print(request.FILES)

    form = TeamForm(request.POST or None, request.FILES or None)
    try:
        if form.is_valid():
            print(form.cleaned_data)
            team = form.save(commit=False)
            team.leader = request.user.player
            form.save()

            return redirect('teams:list')
        else:
            print(form.errors)
    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})

    return render(request, 'teams/form.html', {'form': form})

@login_required
def show(request, id):
    team = Team.objects.get(id=id)
    return render(request, 'teams/show.html', {'team': team})

@login_required
def update(request, id):
    team = Team.objects.get(id=id)

    form = TeamForm(request.POST or None, request.FILES or None, instance=team)
    if form.is_valid():
        instance = form.save()
        instance.leader = request.user.player
        instance.save()
        return redirect('teams:show', instance.id)
    else:
        print(form.errors)

    return render(request, 'teams/form.html', {'team': team, 'form': form})

@login_required
def set_player_position(request, id, player_id):
    try:
        team = Team.objects.get(id=id)
        player = Player.objects.get(id=player_id)
        player.position = request.POST.get('position')
        player.save()

        return JsonResponse({'success': 'Player position has been set'})
    except Exception as error:
        return JsonResponse({'error': str(error)})

@login_required
def invite_player(request, p_id):
    try:
        player = Player.objects.get(id=p_id)
        PlayerInvite.objects.create(player=player, team=request.user.player.team)
        return redirect('players:list')
    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})


@login_required
def show_team_requests(request):
    try:
        requests = request.user.player.team.teamrequest_set.filter(checked=False)
        return render(request, 'requests/team_player_requests.html', {'requests': requests})
    except Exception as e:
        return redirect('teams:list')

@login_required
def accept_player(request, id):
    player_request = TeamRequest.objects.get(id=id)
    player_request.checked = True
    player_request.save()

    player = player_request.player

    team = request.user.player.team
    team.players.add(player)
    team.save()

    return redirect('teams:show', team.id)

@login_required
def reject_player(request, id):
    player_request = TeamRequest.objects.get(id=id)
    player_request.checked = True
    player_request.save()
    team = request.user.player.team

    # we may send an email to notify the player that he's been rejected
    return redirect('teams:team_requests_list')

@login_required
def invite_player_via_email(request, team_id):
    team = Team.objects.get(id=team_id)
    print(request.POST)
    msg = f"You have been Invited to join {team.name}. you can now register here : http://localfootballleague.pythonanywhere.com/ as a player \n Thank your for your time \n best wishes \n Local Football League"
    try:
        send_mail(
            'Team Invitation',
            msg,
            settings.EMAIL_HOST_USER,
            [request.POST.get('email')],
            fail_silently=False,
        )

        return JsonResponse({'success': 'Your invitation has been sent successfully'})

    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})
