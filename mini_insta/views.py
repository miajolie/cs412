from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Profile

# Create your views here.

class ProfileListView(ListView):
    '''Define a view class to obtain data for all Profile records'''

    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"