# project/forms.py
# define the forms that we use for create/update/delete operations
# Author: Mia Batista 

from django import forms
from .models import *


class ShowForm(forms.ModelForm):
    """Form for creating or updating a Show"""
    class Meta:
        model = Show
        fields = ["title", "description", "release_year", "genre", "status", "poster_image"]

class WatchForm(forms.ModelForm):
    '''for for create a watched show'''
    class Meta:
        model = Watch
        fields = ["status"]
                
class SeasonForm(forms.ModelForm):
    """Form for creating or updating a Season"""
    class Meta:
        model = Season
        fields = ["season_number", "title"]


class ReviewForm(forms.ModelForm):
    """Form for creating or updating a Review"""
    class Meta:
        model = Review
        fields = ["rating", "text"]


class ListForm(forms.ModelForm):
    """Form for creating or updating a List"""
    class Meta:
        model = List
        fields = ["title", "description"]


class ListEntryForm(forms.ModelForm):
    """Form for adding a Show to a List"""
    class Meta:
        model = ListEntry
        fields = ["show", "position"]