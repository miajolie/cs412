from django.shortcuts import render
from django.views.generic import ListView,DetailView
from .models import Article

import random
# Create your views here.

class ShowALlView(ListView):
    '''Define a view class to show all blog articles.'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

class ArticleView(DetailView):
    '''Display a single article'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" #singular variable name

class RandomArticleView(DetailView):
    '''Display a single article slected at random''' 

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" #singular variable name

    def get_object(self):

        '''return one onstance of the Article object selected at random'''

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article





