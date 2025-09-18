from django.shortcuts import render
from django.http import HttpResponse


import random
import time

# Create your views here.
daily = ["Witch's Brew Stew", "Mummy Wrapped Meatballs", "Ghoul-ash Pasta",
         "Jack-o'-Lantern Burger", "Coffin Quesadilla", "Zombie Finger Sandwiches",
          "Dracula's Delight Sundae"]

daily_details = {
    "Witch's Brew Stew": {"price": 14.50, "details": "Cauldron-simmered, root veggies, herbed broth"},
    "Mummy Wrapped Meatballs": {"price": 12.25, "details": "Puff-pastry bandages, smoky tomato dip"},
    "Ghoul-ash Pasta": {"price": 13.75, "details": "Beef & paprika cream sauce, haunted spirals"},
    "Jack-o'-Lantern Burger": {"price": 12.99, "details": "Pumpkin-orange cheddar grin, chipotle aioli"},
    "Coffin Quesadilla": {"price": 11.25, "details": "Pressed black-tortilla coffin, 3 cheeses, salsa"},
    "Zombie Finger Sandwiches": {"price": 10.50, "details": "Herbed chicken salad, almond nails (not real!)"},
    "Dracula's Delight Sundae": {"price": 8.75, "details": "Vanilla, cherry 'blood' sauce, dark crumble"},
}
menu =  {
        "pizza": {
            "label": "Pumpkin Patch Pizza",
            "price": 13.50
        },
        "burger":{
            "label": "Vampire-Safe Burger (no garlic!)",
            "price": 11.99
        },
        "salad": {
            "label": "Ghostly Caesar",
            "price": 9.25
        },
        "fries": {
            "label": "Phantom Fries",
            "price": 6.25
        },
    }

# The Spooky Spoon
def main(request):

    '''Main page form'''
    template_name = 'restaurant/main.html'
    return render(request,template_name)

def order(request):
    '''order page view port that randomly selects from list of daily items'''
    template_name = 'restaurant/order.html'
    special = random.choice(daily)
    # randomly selects the special of the day, also finds the price
    # by using a dictionary
    
    daily_special = {
        "special_order": special,
        "price": daily_details[special]["price"],
    }

    context = {
        "menu": menu,
        "special" : daily_special
    }

    return render(request,template_name, context)
 
    

def confirmation(request):
    '''Process the form submission, and generate a result'''
    template_name= "restaurant/confirmation.html"

    if request.POST:
        #extracts form fields into variables:
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']

    # local variables that hold the price and the order
    order= []
    total = 0

    # "order_NAME" will match the name for the checked boxes in the html 
    if 'order_pizza' in request.POST:
        order.append({"name": menu['pizza']['label'], "price": menu['pizza']['price']})
        total += menu['pizza']['price']
    if 'order_burder' in request.POST:
        order.append({"name": menu['burger']['label'], "price": menu['burger']['price']})
        total += menu['burger']['price']
    if 'order_salad' in request.POST:
        order.append({"name": menu['salad']['label'], "price": menu['salad']['price']})
        total += menu['salad']['price']
    if 'order_fries' in request.POST:
        order.append({"name": menu['fries']['label'], "price": menu['fries']['price']})
        total += menu['fries']['price']
    # special added to order
    if 'item_special' in request.POST:
        special = request.POST['special_name']
        special_price = daily_details[special]['price']
        order.append({"name": special, "price": daily_details[special]['price']})
        total += special_price


    minutes_out = random.randint(30, 60)
    time_sec = time.time()
    current_time = 60 * time_sec
    ready_at = current_time + minutes_out
    # convert the time into an actual legible time
    ready_str = time.strftime("%H: %M: %S %p",time.localtime(ready_at))

    context = {
        'name' : name,
        'phone' : phone,
        'email' : email,
        "items": order,
        "total": round(total, 2),
        "ready_at": ready_str,
        "minutes_out": minutes_out,
    }
        

    return render(request, template_name=template_name, context=context)
