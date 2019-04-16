from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from core.models import User
from django.conf import settings
from django.core.mail import send_mail
from .models import ParticipateInvite
from teams.models import PlayerInvite
from leagues.models import League, FieldReseravtion
from core.decorators import *



@login_required
def invite_requests(request):
        requests = request.user.participateinvite_set.filter(checked=False)
        return render(request, 'requests/list.html', {'requests': requests})

@login_required
@check_admin
def list_landlords(request, id):
    league = League.objects.get(id=id)
    field_reservation = FieldReseravtion.objects.filter(league=league, is_paid=False)
    return render(request, 'payment/landlords.html',  {'field_reservations': field_reservation, 'league': league})

@login_required
@check_team_leader
def accept_invite_as_team(request, id):
    invite_request = ParticipateInvite.objects.get(id=id)
    return redirect('payment:process', id=invite_request.id)


@login_required
@check_team_leader
def reject_invite_as_team(request, id):
    invite_request = ParticipateInvite.objects.get(id=id)
    invite_request.checked = True
    league = invite_request.league
    league.teams.remove(invite_request.team)
    invite_request.delete()


    #send email to the site admin
    msg = f"{invite_request.team} has rejected your invitation to join {invite_request.league.name}"
    try:
        send_mail(
            'Team Reject Your Request',
            msg,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})


    return redirect('league:requests')


@login_required
@check_sponsor
def accept_invite_as_sponsor(request, id):
    invite_request = ParticipateInvite.objects.get(id=id)
    return redirect('payment:process', id=invite_request.id, flag='sponsor')


@login_required
@check_sponsor
def reject_invite_as_sponsor(request, id):
    invite_request = ParticipateInvite.objects.get(id=id)
    invite_request.checked = True
    league = invite_request.league
    league.sponsor = None
    league.save()
    invite_request.delete()



    #send email to the site admin
    msg = f"{invite_request.league.sponsor} has rejected your sponsorship invitation to {invite_request.league.name}"
    try:
        send_mail(
            'Sponsor Reject Your Request',
            msg,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})


    return redirect('league:requests')


@login_required
@check_landlord
def accept_invite_as_landlord(request, id):
    invite_request = ParticipateInvite.objects.get(id=id)
    invite_request.checked = True
    field = invite_request.match.location
    field.is_available = False
    field.save()
    field_reservation = FieldReseravtion.objects.create(league=invite_request.league,
                                                        match=invite_request.match,
                                                        landlord=invite_request.participant)
    print(field_reservation )
    invite_request.save()

    return redirect('league:requests')


@login_required
@check_landlord
def reject_invite_as_landlord(request, id):
    invite_request = ParticipateInvite.objects.get(id=id)
    invite_request.checked = True
    match = invite_request.match
    match.location = None
    match.save()
    invite_request.delete()

    # send email to the site admin
    msg = f"{invite_request.match.location.owner.user} has rejected your reservation of his own field regarding {invite_request.league.name}"
    try:
        send_mail(
            'Landlord Reject Your Request',
            msg,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})



    return redirect('league:requests')