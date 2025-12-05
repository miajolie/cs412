# project/urls.py
# all urls needed for the project
# Author: Mia Batista

from django.urls import path 
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


urlpatterns=[
    # auth
    path("login/",  auth_views.LoginView.as_view(template_name="project/login.html"), name="login"),

    path("logout/", auth_views.LogoutView.as_view(next_page = "logout_confirmation"), name="logout"),

    path("logged-out/", TemplateView.as_view(template_name="project/logged_out.html"),name="logout_confirmation"),

    path("signup/", views.signup_view, name="signup"),

    # home path 
    path('', views.HomeView.as_view(), name='home'),

    # viewer
    path("profile/", views.ViewerProfileView.as_view(), name="viewer_profile"),

    # watch
    path("show/<int:show_id>/watch/add/", views.WatchCreateView.as_view(),name="watch_add"),
    path("watch/<int:pk>/edit/",views.WatchUpdateView.as_view(),name="watch_update"),

    #shows urls
    path('shows/', views.ShowListView.as_view(), name='show_list'),
    path('shows/<int:pk>/', views.ShowDetailView.as_view(), name='show_detail'),
    path('shows/create/', views.ShowCreateView.as_view(), name='show_create'),
    path('shows/<int:pk>/update/', views.ShowUpdateView.as_view(), name='show_update'),
    path('shows/<int:pk>/delete/', views.ShowDeleteView.as_view(), name='show_delete'),
    path("my_shows/<int:pk>/",views.ShowReviewPageView.as_view(),name="show_review_page"),


    # seasons urls
    path('shows/<int:show_id>/seasons/create/', views.SeasonCreateView.as_view(), name='season_create'),
    path('seasons/<int:pk>/update/', views.SeasonUpdateView.as_view(), name='season_update'),
    path('seasons/<int:pk>/delete/', views.SeasonDeleteView.as_view(), name='season_delete'),

    # Reviews urls
    path('shows/<int:show_id>/reviews/create/', views.ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/update/', views.ReviewUpdateView.as_view(), name='review_update'),
    path('reviews/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),



    # Lists urls 
    path('lists/', views.ListListView.as_view(), name='list_list'),
    path('lists/create/', views.ListCreateView.as_view(), name='list_create'),
    path('lists/<int:pk>/', views.ListDetailView.as_view(), name='list_detail'),
    path('lists/<int:pk>/update/', views.ListUpdateView.as_view(), name='list_update'),
    path('lists/<int:pk>/delete/', views.ListDeleteView.as_view(), name='list_delete'),

    # ListEntries urls
    path('lists/<int:list_id>/add/', views.ListEntryCreateView.as_view(), name='listentry_create'),
    path('listentries/<int:pk>/delete/', views.ListEntryDeleteView.as_view(), name='listentry_delete'),



]