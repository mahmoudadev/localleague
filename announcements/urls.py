from django.urls import path, include
from . import views

announcements_urlpatterns = ([

                                 path('', views.list, name='list'),
                                 path('<int:id>/', views.item, name='item'),

                             ], 'announcements')





urlpatterns = [
    path('', include(announcements_urlpatterns)),
]
