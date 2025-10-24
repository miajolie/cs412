# mini_insta/forms.py
# define the forms that we use for create/update/delete operations

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    '''a form to add a post to the database '''

    class Meta:
        '''associate this form with a model from our database'''
        model= Post 
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    '''a form to update a profile'''

    class Meta:
        '''associate this form with a model from our database'''
        model = Profile
        fields = ['display_name', 'bio_text', 'profile_image_url']

class UpdatePostForm(forms.ModelForm):
    '''a form to update a post'''

    class Meta:
        '''associate this form with a model from our database'''
        model = Post
        fields = ['caption']

class  CreateProfileForm(forms.ModelForm):
    '''a form to create a user'''

    class Meta:
        '''associate this form with a model from our database'''

        model = Profile
        fields = ['username', 'display_name', 'bio_text', 'profile_image_url']





    
