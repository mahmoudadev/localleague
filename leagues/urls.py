from django.urls import path, include
from . import views

league_urlpatterns = ([

                          path('invitations', views.invite_requests, name='requests'),

                          path('team/<int:id>/accept/', views.accept_invite_as_team, name='team_accept'),
                          path('team/<int:id>/reject/', views.reject_invite_as_team, name='team_reject'),
                          path('sponsor/<int:id>/accept/', views.accept_invite_as_sponsor, name='sponsor_accept'),
                          path('sponsor/<int:id>/reject/', views.reject_invite_as_sponsor, name='sponsor_reject'),
                          path('landlord/<int:id>/accept/', views.accept_invite_as_landlord, name='landlord_accept'),
                          path('landlord/<int:id>/reject/', views.reject_invite_as_landlord, name='landlord_reject'),

                        path('<int:id>/league_landlords/', views.list_landlords , name='list_landlords'),

                      ], 'league')

urlpatterns = [
    path('', include(league_urlpatterns))
]
