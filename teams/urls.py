from django.urls import path, include
from . import views

teams_urlpatterns = ([

                         path('', views.list, name='list'),

                         path('team_requests/', views.show_team_requests, name='team_requests_list'),

                         path('create/', views.create, name='create'),

                         path('invite_player/<int:p_id>/', views.invite_player, name='invite_player'),

                         path('player_request/<int:id>/accept', views.accept_player, name='accept_player'),

                         path('player/<int:id>/reject', views.reject_player, name='reject_player'),



                         path('<int:id>/', include([

                             path('', views.show, name='show'),

                             path('edit/', views.update, name='update'),

                             path('set_player_position/<int:player_id>/', views.set_player_position,
                                  name='set_player_pos'),

                         ]))

                     ], 'teams')

urlpatterns = [
    path('', include(teams_urlpatterns))
]
