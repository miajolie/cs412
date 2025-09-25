from django.urls import path 
from .views import ShowALlView, ArticleView, RandomArticleView

urlpatterns=[
    
    path('', RandomArticleView.as_view(), name = "random"),
    path('show_all', ShowALlView.as_view(), name = "show_all"),
    path('article/<int:pk>', ArticleView.as_view(), name='article'),

]