from django.urls import path 
from .views import ProfileListView

urlpatterns=[
    
    path('', ProfileListView.as_view(), name = "show_all_profiles"),

    # path('', RandomArticleView.as_view(), name = "random"),
    # path('article/<int:pk>', ArticleView.as_view(), name='article'),

]