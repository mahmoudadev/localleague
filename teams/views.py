from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect

from core.models import Player
from .forms import  TeamForm
from teams.models import Team, PlayerInvite, TeamRequest





def list(request):
    teams = Team.objects.all()
    return render(request, 'teams/list.html', {'teams': teams})




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



def show(request, id):
    team = Team.objects.get(id=id)
    return render(request, 'teams/show.html', {'team': team })


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


def set_player_position(request, id ,  player_id):
    try:
        team = Team.objects.get(id=id)
        player = Player.objects.get(id=player_id)
        player.position = request.POST.get('position')
        player.save()

        return JsonResponse({'success': 'Player position has been set'})
    except Exception as error:
        return JsonResponse({'error': str(error)})


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


def accept_player(request, id):
    player_request = TeamRequest.objects.get(id=id)
    player_request.checked = True
    player_request.save()

    player = player_request.player

    team = request.user.player.team
    team.players.add(player)
    team.save()

    return redirect('teams:show', team.id)


def reject_player(request, id):
    player_request = TeamRequest.objects.get(id=id)
    player_request.checked = True
    player_request.save()
    team = request.user.player.team

    #we may send an email to notify the player that he's been rejected
    return redirect('teams:team_requests_list')