from django.urls import path, include
from . import  views


core_urlpatterns = ([
    path('', views.home , name='home'),
    path('contact/', views.contact , name='contact'),
    path('about/', views.about , name='about'),

], 'core')

urlpatterns = [
    path('', include(core_urlpatterns))
]