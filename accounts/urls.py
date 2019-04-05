from django.urls import path , include
from . import  views

accounts_urlpatterns = ([

    path('signup/', views.signup, name='signup'),

    path('profile/', views.profile, name='profile'),

    path('profile/edit', views.edit, name='edit_profile'),


], 'accounts')


urlpatterns = [

    path('', include(accounts_urlpatterns)),

]