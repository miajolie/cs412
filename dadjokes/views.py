from django.shortcuts import render
from .models import Joke, Picture
from django.views.generic import DetailView

# Create your views here.

def random(request):
    '''displays one joke and picture at random'''
    template_name = "dadjokes/random.html"

    joke = Joke.objects.order_by("?").first()
    picture = Picture.objects.order_by("?").first()

    context = {

        "joke": joke, "picture": picture
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
