from django.shortcuts import render
from django.http import HttpResponse
import random
# Create your views here.
daily = ["Witch's Brew Stew", "Mummy Wrapped Meatballs", "Ghoul-ash Pasta",
         "Jack-o'-Lantern Burger", "Coffin Quesadilla", "Zombie Finger Sandwiches",
          "Dracula's Delight Sundae"]

# The Spooky Spoon
def main(request):

    '''Main page form'''
    template_name = 'restaurant/main.html'
    return render(request,template_name)

def order(request):
    '''order page view port that randomly selects from list of daily items'''
    template_name = 'restaurant/order.html'
    
    # randomly selects the special of the day
    context = {
        "special" : random.choice(daily)
    }

    return render(request,template_name, context)
 
    

def submit(request):
    '''Process the form submission, and generate a result'''
    template_name= "restaurant/confirmation.html"

    if request.POST:
        #extracts form fields into variables:
        name = request.POST['name']
        favorite_color= request.POST ['favorite_color']

    context={
        'name' : name,
        'favorite_color': favorite_color
    }
    return render(request, template_name=template_name, context=context)
