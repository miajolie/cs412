# dadjokes/urls.py
# holds all the urls for the dadjokes app django application 
# Mia Jolie Batista

from django.urls import path 
from . import views
from .views import JokeDetailView, PictureDetailView

urlpatterns = [


    path("", views.random_list, name="home"),
    path("random", views.random_list, name="random"),
    path("jokes", views.jokes, name="jokes"),
    path("joke/<int:pk>", JokeDetailView.as_view(), name="joke_detail"),
    path("pictures", views.pictures, name="pictures"),
    path("picture/<int:pk>", PictureDetailView.as_view(), name="picture_detail"),

    # API URLS
    path("api/", views.RandomJokeAPI.as_view(), name="api_home"),
    path("api/random", views.RandomJokeAPI.as_view(), name="api_random_joke"),
    path("api/random_picture", views.RandomPictureAPI.as_view(), name="api_random_picture"),
    path("api/jokes", views.JokeListAPI.as_view(), name="api_jokes"),
    path("api/joke/<int:pk>", views.JokeDetailAPI.as_view(), name="api_joke_detail"),
    path("api/pictures", views.PictureListAPI.as_view(), name="api_pictures"),
    path("api/picture/<int:pk>", views.PictureDetailAPI.as_view(), name="api_picture_detail"),
]



