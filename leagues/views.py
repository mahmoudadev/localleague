from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.models import User
from .models import ParticipateInvite
from teams.models import PlayerInvite
from leagues.models import League

@login_required
def invite_requests(request):
    if request.user.user_type == 'player':
        print('player')
        requests = request.user.player.playerinvite_set.filter(checked=False)
        print(requests)
        return render(request, 'requests/team_join_requests.html', {'requests': requests})
    else:
        requests = request.user.participateinvite_set.filter(checked=False)
        return render(request, 'requests/list.html', {'requests': requests})

def list_landlords(request, id):
    league = League.objects.get(id=id)
    landlords = league.get_landlords()

    print(landlords)

    return render(request, 'payment/landlords.html',  {'landlords': landlords, 'league': league})

def accept_invite_as_team(request, id):
    invite_request = ParticipateInvite.objects.get(id=id)
    return redirect('payment:process', id=invite_request.id)



def reject_invite_as_team(request, id):
    invite_request = ParticipateInvite.objects.get(id=id)
    invite_request.checked = True
    league = invite_request.league
    league.teams.remove(invite_request.team)
    league.save()
    invite_request.delete()

    return redirect('league:requests')

def accept_invite_as_sponsor(request, id):
    invite_request = ParticipateInvite.objects.get(id=id)
    return redirect('payment:process', id=invite_request.id, flag='sponsor')



def reject_invite_as_sponsor(request, id):
    invite_request = ParticipateInvite.objects.get(id=id)
    invite_request.checked = True
    league = invite_request.league
    league.sponsor = None
    league.save()
    invite_request.delete()
    return redirect('league:requests')



def accept_invite_as_landlord(request, id):
    invite_request = ParticipateInvite.objects.get(id=id)
    invite_request.checked = True
    invite_request.save()

    return redirect('league:requests')



def reject_invite_as_landlord(request, id):
    invite_request = ParticipateInvite.objects.get(id=id)
    invite_request.checked = True
    match = invite_request.match
    match.location = None
    match.save()
    invite_request.delete()
    return redirect('league:requests')