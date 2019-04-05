from django.urls import path, include
from . import views


players_urlpatterns = ([

        path('<int:id>/', views.player_profile, name='show_profile'),

], 'players')




urlpatterns = [
    path('', include(players_urlpatterns))
]