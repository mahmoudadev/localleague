from django.shortcuts import render
from core.models import User

def player_profile(request, id):
    person = User.objects.get(id=id)
    return render(request, 'accounts/show.html', {'person': person })
