from django.urls import path , include
from . import  views

accounts_urlpatterns = ([

    path('signup/', views.signup, name='signup'),


], 'accounts')


urlpatterns = [

    path('', include(accounts_urlpatterns)),

]