from django.shortcuts import render, redirect
from .forms import RegistraionForm
from django.contrib.auth import authenticate, login

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