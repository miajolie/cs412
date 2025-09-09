from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.

quotes = ["Wikipedia is the best thing ever. Anyone in the world can write anything they want about any subject so you know you are getting the best possible information.",
          "I’m an early bird and I’m a night owl so I’m wise and I have worms.",
          "You know what they say. Fool me once, strike one, but fool me twice...strike three."]
images = ["https://miro.medium.com/v2/resize:fit:1400/format:webp/1*caByH6RLCHxfGvDewB7Faw.jpeg",
          "https://upload.wikimedia.org/wikipedia/en/d/dc/MichaelScott.png",
          "https://img.pastemagazine.com/wp-content/uploads/2022/06/20161933/6110WZf33tL._SL1200_.jpg"]


def quote_page(request):
    """"Respond to the URL 'quote', delegate work to a template"""

    template_name= 'quotes/quote.html'
    # might have same template name in multiple apps and its important to have the directory included 

    # dict of context variables
    context= {
        
        # "time" : time.ctime(),
        # "letter1": chr(random.randint(65,90)),
        # "letter2": chr(random.randint(65,90)),
        # "number": random.randint(1,10),
        }

    return render(request, template_name, context)

def about_page(request):
    """"Respond to the URL 'about', delegate work to a template"""

    template_name= 'quotes/about.html'
    # might have same template name in multiple apps and its important to have the directory included 

    # dict of context variables
    context= {
        
        # "time" : time.ctime(),
        # "letter1": chr(random.randint(65,90)),
        # "letter2": chr(random.randint(65,90)),
        # "number": random.randint(1,10),
        }

    return render(request, template_name, context)

def about_page(request):
    """"Respond to the URL 'show_all', delegate work to a template"""

    template_name= 'quotes/show_all.html'
    # might have same template name in multiple apps and its important to have the directory included 

    # dict of context variables
    context= {
        
        # "time" : time.ctime(),
        # "letter1": chr(random.randint(65,90)),
        # "letter2": chr(random.randint(65,90)),
        # "number": random.randint(1,10),
        }

    return render(request, template_name, context)


