from django.shortcuts import render
from announcements.models import Announcement
from leagues.models import League

def home(request):
    news = Announcement.objects.all().order_by("-id")
    events = League.objects.all()

    return render(request, 'homepage.html', {'news': news, 'events':events })



def post_page(request, id):
    post = Announcement.objects.get(id=id)
    return render(request, 'announcements/single.html', {'post': post})


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')