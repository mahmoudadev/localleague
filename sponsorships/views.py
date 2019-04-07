from django.shortcuts import render
from sponsorships.models import SponsorshipPackge


def list(request):
    packages = SponsorshipPackge.objects.all()

    return render(request, 'sponsorships/sponsorships.html', {'packages': packages})



def subscribe(request, id):
    packages = SponsorshipPackge.objects.all()
    return render(request, 'sponsorships/sponsorships.html', {'packages': packages })
