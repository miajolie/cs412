# define the forms that we use for create/update/delete operations

from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    '''A form to add an Article to the database'''

    class Meta:
        '''associate this form with a model from our database'''
        model= Article 
        fields = ['author','title', 'text', 'image_url']

class CreateCommentForm(forms.ModelForm):
    '''A fom to add a comment about an article'''

    class Meta:
        '''associate this form with a model from our database'''

        model = Comment
        # fields = ['article', 'author', 'text'] new version below to not do the scroll feature to 
        # pick which article you ant to attach it to 
        fields = ['author', 'text']
