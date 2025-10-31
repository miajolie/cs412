# voter_analytics/views.py
# author: Mia Batista 
# displays all the views for the voter site


from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Count
from .models import Voter
from .forms import VoterForm

import plotly
import plotly.graph_objects as go

# Create your views here.
def apply_filters(qs, request):
    """Filter queryset based on GET params"""
    #request = self.request 

    GET = request.GET

    # party filter

    if 'party' in GET:
        party = GET['party']
        if party:
            # matches both 'U' and 'U ' !
            qs = qs.filter(party__istartswith=party)

    # birth year bounds 
    min_birth = GET.get('min_birth_year', '')
    max_birth = GET.get('max_birth_year', '')
    if min_birth:
        qs = qs.filter(date_of_birth__year__gte=int(min_birth))
    if max_birth:
        qs = qs.filter(date_of_birth__year__lte=int(max_birth))

    # voter score
    if 'voter_score' in GET:
        voter_score = GET['voter_score']
        if voter_score != '':
            qs = qs.filter(voter_score=int(voter_score))


    # election checkboxes 
    for flag in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
        if GET.get(flag):
            qs = qs.filter(**{flag: True})

    return qs


class VoterListView(ListView):
    '''View to display voter results'''
    template_name = 'voter_analytics/voter_listing.html'
    model = Voter
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        qs = Voter.objects.all().order_by('last_name','first_name')
        return apply_filters(qs, self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VoterForm(self.request.GET)

        # necessary code in order to carry filters to second page
        q = self.request.GET.copy()
        q.pop('page', None)                 
        context['querystring'] = q.urlencode()
        
        return context


class VoterDetailView(DetailView):
    '''view to display one voter'''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'

    def get_context_data(self, **kwargs):
        '''helps with google map functionality'''

        context = super().get_context_data(**kwargs)
        person = context['voter']
        addr = f"{person.street_number} {person.street_name}"
        if person.apartment_number:
            addr += f" Apt {person.apartment_number}"
        if person.zip_code:
            addr += f", {person.zip_code}"
        context['maps_query'] = addr

        return context

class GraphsView(ListView):
    '''view to display the graphs for voter data'''

    template_name = 'voter_analytics/graphs.html'
    model = Voter
    context_object_name = 'voters'

    def get_queryset(self):
        """Re-use filtering from Task 2"""
        qs = Voter.objects.all()
        return apply_filters(qs, self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = context['voters']

        # form field
        context['form'] = VoterForm(self.request.GET)

        # Histogram
        birth_years = (
            qs.exclude(date_of_birth__isnull=True)
              .values('date_of_birth__year')
              .annotate(count=Count('id'))
              .order_by('date_of_birth__year')
        )
        x = [r['date_of_birth__year'] for r in birth_years]
        y = [r['count'] for r in birth_years]
        context['birth_year_hist'] = plotly.offline.plot(
            {"data":[go.Bar(x=x, y=y)],
             "layout_title_text":"Voters by Birth Year"},
            auto_open=False, output_type="div"
        )

        # Party Pie Chart 
        parties = qs.values('party').annotate(count=Count('id')).order_by('party')
        labels = [(p['party'] or '').strip() or 'Unknown' for p in parties]
        values = [p['count'] for p in parties]
        context['party_pie'] = plotly.offline.plot(
            {"data":[go.Pie(labels=labels, values=values)],
             "layout_title_text":"Party Affiliation"},
            auto_open=False, output_type="div"
        )

        # Election Participation
        elections = ['v20state','v21town','v21primary','v22general','v23town']
        counts = [qs.filter(**{e: True}).count() for e in elections]
        context['election_bar'] = plotly.offline.plot(
            {"data":[go.Bar(x=elections, y=counts)],
             "layout_title_text":"Participation by Election"},
            auto_open=False, output_type="div"
        )

        return context
