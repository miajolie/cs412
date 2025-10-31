# urls.py
# author: Mia Batista 
# all the urls for the voter site, how they all link

from django.urls import path 
from . import views 


urlpatterns = [


    path('', views.VoterListView.as_view(), name="voters"),
    path('voter', views.VoterListView.as_view(), name='voter'),
    path('voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter_detail'),
    path('graphs/', views.GraphsView.as_view(), name='graphs'),


]


