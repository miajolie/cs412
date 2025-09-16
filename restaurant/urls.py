from django.urls import path 
from django.conf import settings
from . import views

urlpatterns = [
    # path(r'', views.show_form, name='show_form'),
    # path(r'submit', views.submit, name='submit'),
    path(r'Home', views.main, name='main_page'),
    path(r'Order Now!', views.order, name='order_page'),
    path(r'Confirm Order', views.confirmation, name = 'confirmation_page')

]