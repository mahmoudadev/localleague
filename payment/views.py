from django.shortcuts import render, reverse
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm

from django.views.decorators.csrf import csrf_exempt

from leagues.models import League


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')




@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')


def payment_process(request, id, flag=None):

    league = League.objects.get(id=id)
    if flag == 'sponsor':
        amount = league.sponsor.package.price
    else:
        amount = league.fees_per_team


    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": amount,
        "item_name": "League Subscription",
        "invoice": league.id ,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment:done')),
        "cancel_return": request.build_absolute_uri(reverse('payment:cancel')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "payment/process.html", context)
