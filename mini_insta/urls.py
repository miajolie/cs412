# all urls needed for the site, so far only home page of all profiles
# and the link for the image to access the individual profile 

from django.urls import path 
from .views import ProfileListView, ProfileDetailView

urlpatterns=[
    
    path('', ProfileListView.as_view(), name = "show_all_profiles"),
    
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),

]