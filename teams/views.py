from django.http import JsonResponse
from django.shortcuts import render, redirect

from core.models import Player
from .forms import  TeamForm
from teams.models import Team





def list(request):
    teams = Team.objects.all()
    return render(request, 'teams/list.html', {'teams': teams})




def create(request):
    print(request.POST)
    print(request.FILES)

    form = TeamForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        print(form.cleaned_data)
        team = form.save(commit=False)
        team.leader = request.user.player
        form.save()

        return redirect('teams:list')
    else:
        print(form.errors)


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