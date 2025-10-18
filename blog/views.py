from django.shortcuts import render
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from .models import Article, Comment
from .forms import CreateArticleForm, CreateCommentForm, UpdateArticleForm
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin ## NEW

from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW

import random
# Create your views here.

class ShowALlView(ListView):
    '''Define a view class to show all blog articles.'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles"

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''
 
        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')
 
 
        return super().dispatch(request, *args, **kwargs)


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


class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Article
    1) display the HTML form to user (GET)
    2) process the form submission and store the new Article object (POST)
    '''

    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def get_login_url(self):
        '''return the URL required for login'''
        return reverse('login')
    
    def form_valid(self, form):
        '''Handle the form submission to create a new Article object.
        Elegant way to find login user and attach it to the article object for the form
        '''


        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')
 
        # find the logged in user
        user = self.request.user
        print(f"CreateArticleView user={user} article.user={user}")
 
        # attach user to form instance (Article object):
        form.instance.user = user
 
        return super().form_valid(form)
        

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

class UpdateArticleView(UpdateView):
    '''A view to update an Article and save it to the database.'''
 
 
    model = Article
    form_class = UpdateArticleForm
    template_name = "blog/update_article_form.html"
    
    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'UpdateArticleView: form.cleaned_data={form.cleaned_data}')
 
 
        return super().form_valid(form)
    
class DeleteCommentView(DeleteView):
    '''A view to delete a comment and remove it from the database.'''
 
    template_name = "blog/delete_comment_form.html"
    model = Comment
    context_object_name = 'comment'   

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
 
 
        # get the pk for this comment
        pk = self.kwargs.get('pk')
        comment = Comment.objects.get(pk=pk)
        
        # find the article to which this Comment is related by FK
        article = comment.article
        
        # reverse to show the article page
        return reverse('article', kwargs={'pk':article.pk})
 
        

class UserRegistrationView(CreateView):
    '''A view to show/process the registration form to create a new User.'''
 
 
    template_name = 'blog/register.html'
    form_class = UserCreationForm
    model = User
    
    def get_success_url(self):
        '''The URL to redirect to after creating a new User.'''
        return reverse('login')