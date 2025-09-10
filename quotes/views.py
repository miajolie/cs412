from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import random

# Create your views here.

quotes = ["Wikipedia is the best thing ever. Anyone in the world can write anything they want about any subject so you know you are getting the best possible information.",
          "Im an early bird and Im a night owl so Im wise and I have worms.",
          "You know what they say. Fool me once, strike one, but fool me twice...strike three."]
images = ["https://miro.medium.com/v2/resize:fit:1400/format:webp/1*caByH6RLCHxfGvDewB7Faw.jpeg",
          "https://upload.wikimedia.org/wikipedia/en/d/dc/MichaelScott.png",
          "https://img.pastemagazine.com/wp-content/uploads/2022/06/20161933/6110WZf33tL._SL1200_.jpg"]


def quote_page(request):
    """"Respond to the URL 'quote', delegate work to a template. Will randomly
    select one quote and one image from the list"""

    template_name= 'quotes/quote.html'
    # might have same template name in multiple apps and its important to have the directory included 

    # dict of context variables
    # here is where I will be handling the random generator for the quotes and images 
    context= {
        "quote" : random.choice(quotes),
        "image" : random. choice(images),
        "person": "Michael Scott"
        }

    return render(request, template_name, context)

def about_page(request):
    """"Respond to the URL 'about', delegate work to a template"""

    template_name= 'quotes/about.html'
    # might have same template name in multiple apps and its important to have the directory included 

    # dict of context variables
    # here is where I will be storing all the important information 
    context = {
        "person": "Michael Scott",
        "bio": "This is the world's greatest boss, brought to you by the world's greatest show: The Office (USA version)",
        "note" : "Hi everyone! This is Mia, and I thought it was important to bring some awareness to some great quotes from Michael Scott for CS412",
        }

    return render(request, template_name, context)

def show_all_page(request):
    """"Respond to the URL 'show_all', delegate work to a template"""

    template_name= 'quotes/show_all.html'
    # might have same template name in multiple apps and its important to have the directory included 

    # dict of context variables
    # here is where I will be handling all the information that should be displaying
    context= {
        "quote": quotes,
        "image": images,
        "person": "Michael Scott"
        }

    return render(request, template_name, context)


