from django.shortcuts import render, redirect
from sponsorships.models import SponsorshipPackge


def list(request):
    packages = SponsorshipPackge.objects.all()

    return render(request, 'sponsorships/sponsorships.html', {'packages': packages})



def subscribe(request, id):
    print('subscribe view')
    package = SponsorshipPackge.objects.get(id=id)
    person = request.user
    person.sponsor.package = package
    person.sponsor.save()

    return redirect('sponsorships:list')
