from django import forms
from .models import *
from datetime import date


class VoterForm(forms.Form):
    '''a form to add a post to the database '''

    current_year = date.today().year
    years = [(y,y) for y in range(1900, current_year + 1)]

    min_birth_year = forms.ChoiceField(
        choices = [('', 'Any')] + years, required=False, label="Born After"
    )

    max_birth_year = forms.ChoiceField(
        choices = [('', 'Any')] + years, required=False, label="Born Before"
    )

    voter_score = forms.ChoiceField(
        choices = [('', 'Any')] + [(x, str(x)) for x in range(6)], required=False, label="Voter Score"
    )

    party = forms.ChoiceField(
        choices = [('', 'Any')], required=False, label="Political"
    )

    v20state = forms.BooleanField(required=False, initial=False,label='v20state')
    v21town = forms.BooleanField(required=False, initial=False,label='v21town')
    v21primary = forms.BooleanField(required=False, initial=False,label='v21primary')
    v22general = forms.BooleanField(required=False, initial=False,label='v22general')
    v23town = forms.BooleanField(required=False, initial= False, label= 'v23town')


    def __init__(self, *args, **kwargs):
        '''wont run code until database is initialized'''
        super().__init__(*args, **kwargs)
        parties = sorted(filter(None, {(p or '').strip() for p in Voter.objects.values_list('party', flat=True).distinct()}))
        self.fields['party'].choices += [(p, p) for p in parties]

