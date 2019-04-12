from django.shortcuts import render
from announcements.models import Announcement

def list(request):
    pass




def item(request):
    item = Announcement.objects.get(id=id)
    return render(request, 'announcements/single.html', {'item': item})




