from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from sponsorships.models import SponsorshipPackge

@login_required
def list(request):
    packages = SponsorshipPackge.objects.all()

    return render(request, 'sponsorships/sponsorships.html', {'packages': packages})


@login_required
def subscribe(request, id):
    try:
        print('subscribe view')
        package = SponsorshipPackge.objects.get(id=id)
        person = request.user
        person.sponsor.package = package
        person.sponsor.save()
        return redirect('sponsorships:list')
    except Exception as e:
        return render(request, 'expections/show.html', {'error': e})