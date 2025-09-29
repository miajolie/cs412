from django.shortcuts import render
from django.views.generic import ListView,DetailView, CreateView
from .models import Article
from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse

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
    '''Display a single article selected at random''' 

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" #singular variable name

    def get_object(self):

        '''return one onstance of the Article object selected at random'''

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article


class CreateArticleView(CreateView):
    '''A view to handle creation of a new Article
    1) display the HTML form to user (GET)
    2) process the form submission and store the new Article object (POST)
    '''

    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

class CreateCommentView(CreateView):
    '''A view to handle creation of a new comment on an article'''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new comment.'''

        # return reverse('show_all') 
    # not ideal but we'll do this for now 
        pk = self.kwargs['pk']
        return reverse('article', kwargs={'pk': pk})

    def get_context_data(self):
        '''return the dictionary of context variaable for is in the template'''

        # calling the superclass method 
        context = super().get_context_data()

        # find/add the article to the context
        # retrive the pj from the url pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        # add this article to the context dictionary 
        context['article'] = article

        return context 

    def form_valid(self, form):

        '''This method handles the form submission and saves the new object to 
        the Django database.We need to add the foreign key (of the Article) to 
        the Commentobject before saving it to the database.'''

        print(form.cleaned_data)
        # retrive the pj from the url pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        # attach this article to the comment
        form.instance.article = article 
        # set the fk 

        # delegate the work to the superclass method form_valid 

        return super().form_valid(form)
