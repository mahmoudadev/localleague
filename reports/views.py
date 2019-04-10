from django.shortcuts import render, redirect
from leagues.models import League




def leagues_summary(request):

    leagues = League.objects.all()

    return render(request, 'reports/summary.html', {'leagues': leagues})