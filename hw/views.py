#file:hw/views.py
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random
# Create your views here.
def home(request):
    """Func to respon to the "home" request"""
    
    response_text = f'''
    <html>
    <h1> Hello, world!</h1>
    The current time is {time.ctime()},
    </html>
    '''

    return HttpResponse(response_text)

def home_page(request):
    """"Respond to the URL '', delegate work to a template"""

    template_name= 'hw/home.html'
    # might have same template name in multiple apps and its important to have the directory included 

    # dict of context variables
    context= {
        
        "time" : time.ctime(),
        "letter1": chr(random.randint(65,90)),
        "letter2": chr(random.randint(65,90)),
        "number": random.randint(1,10),
        }

    return render(request, template_name, context)

def about_page(request):
    """"Respond to the URL '', delegate work to a template"""

    template_name= 'hw/about.html'
    # might have same template name in multiple apps and its important to have the directory included 

    # dict of context variables
    context= {
        
        "time" : time.ctime(),
        "letter1": chr(random.randint(65,90)),
        "letter2": chr(random.randint(65,90)),
        "number": random.randint(1,10),
        }

    return render(request, template_name, context)