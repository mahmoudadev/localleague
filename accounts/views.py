from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistraionForm
from django.contrib.auth import authenticate, login
from core.models import User
from accounts.forms import UserProfileForm, PlayerForm, SponsorForm

def signup(request):
    form = RegistraionForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)

        if user:
            login(request, user)
            return redirect('core:home')
        else:
            return render(request, 'registration/signup.html',{'form': form })


    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile(request):
    person = request.user
    return render(request, 'players/show.html', {'person': person})

@login_required
def edit(request):

    person = request.user

    if person.user_type == 'team_leader' or person.user_type == 'player':
        user_form = UserProfileForm(request.POST or None, request.FILES or None, instance=person)
        player_form = PlayerForm(request.POST or None , instance=person.player)
        if user_form.is_valid() and player_form.is_valid():
            user_form.save()
            player_form.save()
            return redirect('accounts:profile')
        return render(request, 'accounts/edit.html', {'person': person, 'user_form': user_form , 'additional_form': player_form})

    elif person.user_type == 'sponsor':
        user_form = UserProfileForm(request.POST or None, request.FILES or None, instance=person)
        sponsor_form = SponsorForm(request.POST or None, request.FILES or None, instance=person.sponsor)
        if user_form.is_valid() and sponsor_form.is_valid():
            user_form.save()
            sponsor_form.save()
            return redirect('accounts:profile')
        return render(request, 'accounts/edit.html',
                      {'person': person, 'user_form': user_form, 'additional_form': sponsor_form})

    else:
        user_form = UserProfileForm(request.POST or None, request.FILES or None, instance=person)
        if user_form.is_valid():
            user_form.save()
            return redirect("accounts:profile")

        return render(request, 'accounts/edit.html',
                      {'person': person, 'user_form': user_form })