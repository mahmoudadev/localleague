from django.urls import path, include
from . import views

teams_urlpatterns = ([

                         path('', views.list, name='list'),

                         path('create/', views.create, name='create'),

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
