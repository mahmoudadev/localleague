from django.urls import path, include
from . import views


fields_urlpatterns = ([

        path('', views.list , name='list'),

        path('<int:id>/', views.show , name='show'),

        path('<int:id>/edit', views.edit , name='edit'),

        path('create/', views.create , name='create')


], 'fields')




urlpatterns = [
    path('', include(fields_urlpatterns))
]