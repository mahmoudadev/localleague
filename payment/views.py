from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

from leagues.models import League, ParticipateInvite, FieldReseravtion
from fields.models import Field


@login_required
@csrf_exempt
def payment_done(request, id):
    invite_request = ParticipateInvite.objects.get(id=id)
    invite_request.checked = True
    invite_request.save()

    if request.user.user_type == 'team_leader':
        msg = f"Congrats!, your team leader has accepted invitation to participate on {invite_request.league.name} which will be started at {invite_request.league.starts_at}. \n description: \n {invite_request.league.description} \n Thank you for using our league system \n Local Football League."
        try:
            for player in request.user.player.team.players.all():
                send_mail(
                    'Be Ready!, Your Team Accepted a New League',
                    msg,
                    settings.EMAIL_HOST_USER,
                    [player.user.email],
                    fail_silently=False,
                )
        except Exception as e:
            return render(request, 'expections/show.html', {'error': e})

    return render(request, 'payment/done.html')


@login_required
@csrf_exempt
def admin_payment_done(request, id):
    field_reservation = FieldReseravtion.objects.get(id=id)
    field_reservation.is_paid = True
    field_reservation.save()
    return render(request, 'payment/done.html')


@login_required
@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')


@login_required
def payment_process(request, id, flag=None):
    try:
        invite_request = ParticipateInvite.objects.get(id=id)
        league = invite_request.league
        if flag == 'sponsor':
            amount = league.sponsor.package.price
        else:
            amount = league.fees_per_team
    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})

    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": amount,
        "item_name": "League Subscription",
        "invoice": league.id,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment:done', kwargs={'id': invite_request.id})),
        "cancel_return": request.build_absolute_uri(reverse('payment:cancel')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment/process.html", context)


@login_required
def admin_payment_process(request, id):
    try:
        field_reservation = FieldReseravtion.objects.get(id=id)
        league = field_reservation.league
        field = field_reservation.match.location

    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})

    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": field.price,
        "item_name": "Field Reservation fees",
        "invoice": league.id,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment:admin_done', kwargs={'id': field_reservation.id})),
        "cancel_return": request.build_absolute_uri(reverse('payment:cancel')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment/process.html", context)
