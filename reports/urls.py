from django.urls import path, include
from . import views


reports_urlpatterns = ([


    path('leagues_summary/', views.leagues_summary , name='leagues_summary'),


                       ], 'reports')





urlpatterns = [

    path('', include(reports_urlpatterns)),
]
