from django.urls import path, include
from . import views



sponsorship_urlpattrens = ([


    path('list/', views.list, name='list'),
    path('subscribe/<int:id>', views.subscribe, name='subscribe')

], 'sponsorships')



urlpatterns = [
    path('', include(sponsorship_urlpattrens))
]



