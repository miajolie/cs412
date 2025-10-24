from django.urls import path 
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.main, name='main_page'),

    path(r'home', views.main, name='main_page'),
    path(r'order_now!', views.order, name='order_page'),
    path(r'confirm_order', views.confirmation, name = 'confirmation_page')

]