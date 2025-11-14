# dadjokes/views.py
# holds all the views for the dadjokes app, django application 
# Mia Jolie Batista


from django.shortcuts import render
from .models import Joke, Picture
from django.views.generic import DetailView

from rest_framework import generics
from .serializers import *
from rest_framework.response import Response

# Create your views here.

def random_list(request):
    '''displays one joke and picture at random'''

    # maybe i should do a class and call the random choice 
    # on the get_context_data method to do it that way???

    template_name = "dadjokes/random.html"

    joke = Joke.objects.order_by("?").first()
    picture = Picture.objects.order_by("?").first()

    context = {

        "joke": joke, 
        "picture": picture

    }

    return render(request, template_name=template_name, context=context)

def jokes(request):
    '''displays all jokes, no pictures'''

    jokes = Joke.objects.order_by("-timestamp")

    context = {
        'jokes': jokes,
    }

    return render(request, template_name="dadjokes/jokes.html", context=context)


class JokeDetailView(DetailView):
    '''get one joke'''
    model = Joke
    template_name = "dadjokes/joke_detail.html"
    context_object_name = "joke"

    def get_object(self):
        '''gets the joke based on primary key'''
        pk = self.kwargs.get("pk")
        return Joke.objects.get(pk=pk)
    

def pictures(request):
    '''displays all pictures, no jokes'''

    pictures = Picture.objects.order_by("-timestamp")

    context = {
        'pictures': pictures,
    }

    return render(request, template_name="dadjokes/pictures.html", context=context)

class PictureDetailView(DetailView):
    '''displays one picture based on primary key'''

    model = Picture
    template_name = "dadjokes/picture_detail.html"
    context_object_name = "picture"

    def get_object(self):
        '''gets the joke based on primary key'''
        pk = self.kwargs.get("pk")
        return Picture.objects.get(pk=pk)
    

# API VIEWS

class RandomJokeAPI(generics.RetrieveAPIView):
    '''An API view to return a random joke'''
    serializer_class = JokeSerializer
    queryset = Joke.objects.all()   

    def get_object(self):
        obj = self.get_queryset().order_by("?").first()
        return obj


class RandomPictureAPI(generics.RetrieveAPIView):
    '''An API view to return a random picture'''
    serializer_class = PictureSerializer
    queryset = Picture.objects.all()

    def get_object(self):
        obj = self.get_queryset().order_by("?").first()
        return obj

class JokeListAPI(generics.ListCreateAPIView):
    '''An API view to return a list of jokes'''
    serializer_class = JokeSerializer
    queryset = Joke.objects.order_by("-timestamp")

class JokeDetailAPI(generics.RetrieveAPIView):
    '''An API view to return a jokes'''
    serializer_class = JokeSerializer
    queryset = Joke.objects.all()

class PictureListAPI(generics.ListCreateAPIView):
    '''An API view to return a list of picture'''
    serializer_class = PictureSerializer
    queryset = Picture.objects.order_by("-timestamp")

class PictureDetailAPI(generics.RetrieveAPIView):
    '''An API view to return a picture'''
    serializer_class = PictureSerializer
    queryset = Picture.objects.all()




