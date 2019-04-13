from django.shortcuts import render, reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm

from django.views.decorators.csrf import csrf_exempt

from leagues.models import League, ParticipateInvite, FieldReseravtion
from fields.models import Field

@csrf_exempt
def payment_done(request, id):
    invite_request = ParticipateInvite.objects.get(id=id)
    invite_request.checked = True
    invite_request.save()
    return render(request, 'payment/done.html')


@csrf_exempt
def admin_payment_done(request, id):
    field_reservation = FieldReseravtion.objects.get(id=id)
    field_reservation.is_paid = True
    field_reservation.save()
    return render(request, 'payment/done.html')



@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')


def payment_process(request, id, flag=None):
    try:
        invite_request = ParticipateInvite.objects.get(id=id)
        league = invite_request.league
        if flag == 'sponsor':
            amount = league.sponsor.package.price
        else:
            amount = league.fees_per_team
    except Exception as e:
        return render(request, 'expections/show.html',  {'error': e })

    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": amount,
        "item_name": "League Subscription",
        "invoice": league.id ,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment:done', kwargs={'id': invite_request.id } )),
        "cancel_return": request.build_absolute_uri(reverse('payment:cancel')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment/process.html", context)



def admin_payment_process(request, id):
    try:
        field_reservation = FieldReseravtion.objects.get(id=id)
        league = field_reservation.league
        field = field_reservation.match.location

    except Exception as e:
        return render(request, 'expections/show.html',  {'error': e })

    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": field.price,
        "item_name": "Field Reservation fees",
        "invoice": league.id ,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment:admin_done', kwargs={'id': field_reservation.id})),
        "cancel_return": request.build_absolute_uri(reverse('payment:cancel')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment/process.html", context)
