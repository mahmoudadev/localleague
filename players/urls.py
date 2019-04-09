from django.urls import path, include
from . import views


players_urlpatterns = ([

        path('', views.list, name='list'),
        path('<int:id>/', views.player_profile, name='show_profile'),
        path('team_request/<int:id>/', views.team_request, name='team_request'),
        path('player/<int:id>/accept', views.accept_invite, name='accept_invite'),
        path('player/<int:id>/reject', views.reject_invite, name='reject_invite'),

], 'players')




urlpatterns = [
    path('', include(players_urlpatterns))
]