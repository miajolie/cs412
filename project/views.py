# project/views.py
# all the views of my project 
# created by Mia Batista 

from django.shortcuts import render, redirect
from .models import Show, Season, Review, List, ListEntry, Viewer, Watch
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .forms import ShowForm, SeasonForm, ReviewForm, ListForm, ListEntryForm, WatchForm, ViewerUpdateForm

# Create your views here.

def signup_view(request):
    """Allow a new user to sign up and create a Viewer profile."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # create the User
            user = form.save()

            # create the Viewer profile
            Viewer.objects.create(
                user=user,
                display_name=user.username,

            )

            # log in and redirect home
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }

    return render(request, "project/signup.html", context)


class HomeView(TemplateView):
    """Simple homepage"""
    model = Show
    template_name = "project/home.html"
    context_object_name = "shows"
    
    def get_context_data(self, **kwargs):
        '''to show al shows on the homepage'''
        context = super().get_context_data(**kwargs)
        context["shows"] = Show.objects.all()
        return context
    
class ViewerProfileView(LoginRequiredMixin, TemplateView):
    """Profile page for the logged-in viewer: shows & their reviews."""
    template_name = "project/profile.html"

    def get_login_url(self):
        return reverse("login")

    def get_context_data(self, **kwargs):
        '''conext data for a profile'''
        context = super().get_context_data(**kwargs)
        viewer = Viewer.objects.get(user=self.request.user)

        # all shows this viewer created
        shows = Show.objects.filter(created_by=viewer).order_by("title")

        # all reviews this viewer has written (for the bottom section if you want it)
        reviews = Review.objects.filter(viewer=viewer).select_related("show")
        watches = Watch.objects.filter(viewer=viewer).select_related("show").order_by("-added_at")

        # watchlist
        watching = watches.filter(status="W")
        finished = watches.filter(status="F")
        planning = watches.filter(status="P")


        context["viewer"] = viewer
        context["shows"] = shows
        context["reviews"] = reviews
        context['watches'] = watches
        context['watching'] = watching
        context["finished"] = finished
        context["planning"] = planning
        context["planning_count"] = planning.count()
        context["watching_count"] = watches.filter(status="W").count()
        context["finished_count"] = watches.filter(status="F").count()
        return context

class ViewerPublicProfileView(DetailView):
    '''way to see someone elses profile'''
    model = Viewer
    template_name = "project/public_profile.html"
    context_object_name = "viewer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        viewer = self.object

        context["reviews"] = viewer.reviews.all()
        context["watches"] = viewer.watches.all()
        context["created_shows"] = viewer.created_shows.all()

        return context

    
class ViewerUpdateView(LoginRequiredMixin, UpdateView):
    '''view to update a profile'''
    model = Viewer
    form_class = ViewerUpdateForm
    template_name = "project/viewer_form.html"

    def get_login_url(self):
        return reverse("login")

    def get_object(self):
        # always edit the logged-in viewer's profile
        return Viewer.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse("viewer_profile")


class WatchCreateView(LoginRequiredMixin, CreateView):
    '''Add a show to the viewer's watchlist'''
    model = Watch
    form_class = WatchForm
    template_name = "project/watch_form.html"

    def get_login_url(self):
        return reverse("login")
    
    def dispatch(self, request, *args, **kwargs):
        '''prevent adding the same show twice!'''
        viewer = Viewer.objects.get(user = request.user)
        show = Show.objects.get(pk = self.kwargs['show_id'])
        watch = Watch.objects.filter(viewer=viewer, show=show).exists()
        
        if watch:
            # already in portfolio!
            return redirect("viewer_profile")


        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        '''handle saving the show and the viewer'''

        viewer = Viewer.objects.get(user = self.request.user)
        show = Show.objects.get(pk=self.kwargs['show_id'])

        form.instance.viewer = viewer
        form.instance.show = show
        
        return super().form_valid(form)
    
    def get_success_url(self):
        '''if successful....'''
        return reverse("viewer_profile")

class WatchUpdateView(LoginRequiredMixin, UpdateView):
    """Change the status of a watch entry (Watching / Finished)."""
    model = Watch
    form_class = WatchForm
    template_name = "project/watch_form.html"

    def get_login_url(self):
        return reverse("login")

    def get_queryset(self):
        # only let the logged-in viewer edit their own watch entries
        viewer = Viewer.objects.get(user=self.request.user)
        return super().get_queryset().filter(viewer=viewer)

    def get_success_url(self):
        return reverse("viewer_profile")
    
class WatchDeleteView(LoginRequiredMixin, DeleteView):
    """Allow a viewer to remove a show from their profile (delete Watch)"""
    model = Watch
    template_name = "project/watch_confirm_delete.html"

    def get_login_url(self):
        return reverse("login")

    def get_queryset(self):
        """Only allow deletion of Watch rows belonging to logged-in viewer"""
        query = super().get_queryset()
        viewer = Viewer.objects.get(user=self.request.user)
        return query.filter(viewer=viewer)

    def get_success_url(self):
        """After deleting, send them back to their profile page"""
        return reverse("viewer_profile") 


class ShowReviewPageView(LoginRequiredMixin, DetailView):
    """Show a single show with this viewer's review (if it exists)"""
    model = Show
    template_name = "project/show_review_page.html"
    context_object_name = "show"

    def get_login_url(self):
        return reverse("login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        viewer = Viewer.objects.get(user=self.request.user)

        # grab the review for THIS show + THIS viewer, if any
        my_review = Review.objects.filter(
            show=self.object,
            viewer=viewer
        ).first()

        context["viewer"] = viewer
        context["my_review"] = my_review
        return context

class ReviewDetailPageView(DetailView):
    """Show a big poster and a specific review (public viewer)."""
    model = Review
    template_name = "project/review_detail_page.html"
    context_object_name = "review"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show"] = self.object.show
        return context


class ShowListView(ListView):
    '''showing all the shows'''
    model = Show 
    template_name = 'project/show_list.html'
    context_object_name = "shows"

class ShowDetailView(DetailView):
    '''a detailed view of a single show'''

    model = Show
    template_name = "project/show_detail.html"
    context_object_name = "show"

    def get_context_data(self, **kwargs):
        '''getting the seasons and reviews from a show'''
        context = super().get_context_data(**kwargs)
        show = self.get_object()
        context['seasons'] = show.seasons.all()
        context['reviews'] = show.reviews.all()


        return context

class ShowCreateView(LoginRequiredMixin,CreateView):
    '''the creation of a show to the database, only allowed by a logged in user'''

    model = Show
    form_class = ShowForm
    template_name = 'project/show_form.html'

    def get_login_url(self):
        '''only allow logged in users '''
        return reverse('login')
    
    def form_valid(self, form):
        '''form valid method, handles the form submission and saves the new object to 
        the Django database'''
        viewer = Viewer.objects.get(user = self.request.user)
        form.instance.created_by = viewer
        return super().form_valid(form)
    
    def get_success_url(self):
        '''where after creating a form directs the user to'''
        return reverse('show_detail', args=[self.object.pk])


class ShowUpdateView(LoginRequiredMixin, UpdateView):
    '''updates a certain show'''
    model = Show
    template_name = "project/show_form.html"
    form_class = ShowForm

    def get_login_url(self):
        '''only allow logged in users '''
        return reverse('login')
    
    def get_queryset(self):
        '''limit updates to only the shows the logged in user created'''

        query = super().get_queryset()
        viewer = Viewer.objects.get(user=self.request.user)
        return query.filter(created_by = viewer)
    
    def get_success_url(self):
        '''once updated, return to the show detail'''
        return reverse("show_detail", args = [self.object.pk])
    
class ShowDeleteView(LoginRequiredMixin, DeleteView):
    '''deleting a show form view'''
    model = Show
    template_name = "project/show_confirm_delete.html"

    def get_login_url(self):
        '''only allow logged in users '''
        return reverse('login')
    
    def get_queryset(self):
        '''only allow deletion of the viewer created the show'''
        query = super().get_queryset()
        viewer = Viewer.objects.get(user = self.request.user)
        return query.filter(created_by = viewer)
    
    def get_context_data(self, **kwargs):
        '''add the show and its creator ti the template context'''
        context = super().get_context_data(**kwargs)
        context['show'] = self.object
        context['creator'] = self.object.created_by

        return context

    def get_success_url(self):
        '''after deleting, return the the main show list'''
        return reverse('show_list')

class SeasonCreateView(LoginRequiredMixin, CreateView):
    '''view to add a season to a show'''
    
    model=Season
    form_class = SeasonForm
    template_name = 'project/season_form.html'

    def get_login_url(self):
        '''only allow logged in users '''
        return reverse("login")

    def form_valid(self, form):
        '''form valid method, handles the form submission and saves the new season object to 
        the Django database'''
        show_id = self.kwargs['show_id']
        show = Show.objects.get(pk = show_id)
        viewer = Viewer.objects.get(user=self.request.user)
        form.instance.created_by = viewer
        form.instance.show = show
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        '''to get the show pk'''
        context = super().get_context_data(**kwargs)
        context['show'] = Show.objects.get(pk=self.kwargs['show_id'])
        return context
    
    def get_success_url(self):
        '''after creating a season, go back to the show's detail page'''
        return reverse ("show_detail", args = [self.object.show.pk])

class SeasonUpdateView(LoginRequiredMixin, UpdateView):
    '''allow editing the season, only allowed if you created the show'''

    model = Season 
    form_class = SeasonForm
    template_name = 'project/season_form.html'

    def get_login_url(self):
        '''only allow logged in users '''
        return reverse("login")
    
    def get_queryset(self):
        '''limit updates to seasons whose show was created by the logged-in viewer'''
        query = super().get_queryset()
        viewer = Viewer.objects.get(user=self.request.user)
        return query.filter(show__created_by = viewer)
    
    def get_context_data(self, **kwargs):
        '''to get the show pk'''
        context = super().get_context_data(**kwargs)
        season = self.get_object()
        context['show'] = season.show
        return context

    def get_success_url(self):
        '''once updated, return to the show detail'''
        return reverse("show_detail", args = [self.object.show.pk])
    
class SeasonDeleteView(LoginRequiredMixin, DeleteView):
    '''allow deleting a season if you created the show'''

    model = Season
    template_name = 'project/season_confirm_delete.html'

    def get_login_url(self):
        '''only allow logged in users '''
        return reverse('login')
    
    def get_queryset(self):
        '''only allow deletion of the viewer created the show'''
        query = super().get_queryset()
        viewer = Viewer.objects.get(user = self.request.user)
        return query.filter(created_by = viewer)
    

    def get_success_url(self):
        '''after deleting, return the the show detail'''
        return reverse("show_detail", args = [self.object.show.pk])
    


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """Create a review for a show (must be logged in)."""
    model = Review
    form_class = ReviewForm
    template_name = "project/review_form.html"

    def get_login_url(self):
        '''only allow logged in users '''
        return reverse("login")

    def form_valid(self, form):
        '''form valid method, handles the form submission and saves the new review object to 
        the Django database'''
        viewer = Viewer.objects.get(user=self.request.user)
        show_id = self.kwargs["show_id"]
        show = Show.objects.get(pk=show_id)

        form.instance.viewer = viewer
        form.instance.show = show
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        '''to get the show pk'''
        context = super().get_context_data(**kwargs)
        context['show'] = Show.objects.get(pk=self.kwargs['show_id'])
        return context

    def get_success_url(self):
        '''return to show detail after form completes'''
        return reverse("show_detail", args=[self.object.show.pk])
    


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """Allow a viewer to edit only their own reviews."""
    model = Review
    form_class = ReviewForm
    template_name = "project/review_form.html"

    def get_login_url(self):
        '''only allow logged in users '''
        return reverse("login")

    def get_queryset(self):
        """Limit updates to reviews by the logged-in viewer."""
        query = super().get_queryset()
        viewer = Viewer.objects.get(user=self.request.user)
        return query.filter(viewer=viewer)
    
    def get_context_data(self, **kwargs):
        '''pass in context for the review'''
        context = super().get_context_data(**kwargs)
        context["show"] = self.object.show
        return context

    def get_success_url(self):
        '''return to show detail after form completes'''
        return reverse("show_detail", args=[self.object.show.pk])

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    """Allow a viewer to delete only their own reviews."""
    model = Review
    template_name = "project/review_confirm_delete.html"

    def get_login_url(self):
        '''only allow logged in users '''
        return reverse("login")

    def get_queryset(self):
        """Limit deletion to reviews by the logged-in viewer."""
        query = super().get_queryset()
        viewer = Viewer.objects.get(user=self.request.user)
        return query.filter(viewer=viewer)

    def get_success_url(self):
        '''return to show detail after deletes'''
        return reverse("show_detail", args=[self.object.show.pk])
    
class ListListView(ListView):
    """Show all lists (or you can filter by logged-in viewer)."""
    model = List
    template_name = "project/list_list.html"
    context_object_name = "lists"


class ListDetailView(DetailView):
    """Show a single list and its entries."""
    model = List
    template_name = "project/list_detail.html"
    context_object_name = "list"

    def get_context_data(self, **kwargs):
        '''getting entries for the context'''
        context = super().get_context_data(**kwargs)
        context["entries"] = self.object.entries.all().order_by("position", "id")
        return context


class ListCreateView(LoginRequiredMixin, CreateView):
    """Create a new list (must be logged in)."""
    model = List
    form_class = ListForm
    template_name = "project/list_form.html"

    def get_login_url(self):
        '''only allow logged in users '''
        return reverse("login")

    def form_valid(self, form):
        '''form valid method, handles the form submission and saves the new review object to 
        the Django database'''
        viewer = Viewer.objects.get(user=self.request.user)
        form.instance.viewer = viewer
        return super().form_valid(form)

    def get_success_url(self):
        '''return to list detail after form completes'''
        return reverse("list_detail", args=[self.object.pk])


class ListUpdateView(LoginRequiredMixin, UpdateView):
    """Allow a viewer to edit only their own lists."""
    model = List
    form_class = ListForm
    template_name = "project/list_form.html"

    def get_login_url(self):
        '''only allow logged in users '''
        return reverse("login")

    def get_queryset(self):
        """Limit updates to lists owned by the logged-in viewer."""
        query = super().get_queryset()
        viewer = Viewer.objects.get(user=self.request.user)
        return query.filter(viewer=viewer)

    def get_success_url(self):
        '''return to list detail after form completes'''
        return reverse("list_detail", args=[self.object.pk])


class ListDeleteView(LoginRequiredMixin, DeleteView):
    """Allow a viewer to delete only their own lists."""
    model = List
    template_name = "project/list_confirm_delete.html"


    def get_login_url(self):
        '''only allow logged in users '''
        return reverse("login")

    def get_queryset(self):
        """Limit deletion to lists owned by the logged-in viewer."""
        query = super().get_queryset()
        viewer = Viewer.objects.get(user=self.request.user)
        return query.filter(viewer=viewer)
    
    def get_success_url(self):
        '''return to lists after deletes'''
        return reverse("list_list")
    


class ListEntryCreateView(LoginRequiredMixin, CreateView):
    """Add a show to a list (must own the list)."""
    model = ListEntry
    form_class = ListEntryForm
    template_name = "project/listentry_form.html"

    def get_login_url(self):
        '''only allow logged in users '''
        return reverse("login")

    def form_valid(self, form):
        '''form valid method, handles the form submission and saves the new review object to 
        the Django database'''
        viewer = Viewer.objects.get(user=self.request.user)
        list_id = self.kwargs["list_id"]

        # only allow adding to a list the viewer owns
        list_object = List.objects.get(pk=list_id, viewer=viewer)
        form.instance.listed = list_object
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        '''to allow for access to the pk'''
        context = super().get_context_data(**kwargs)
        context["list_id"] = self.kwargs["list_id"]
        return context


    def get_success_url(self):
        '''return to list detail after form completes'''
        return reverse("list_detail", args=[self.object.listed.pk])


class ListEntryDeleteView(LoginRequiredMixin, DeleteView):
    """Allow a viewer to remove shows only from their own lists."""
    model = ListEntry
    template_name = "project/listentry_confirm_delete.html"

    def get_login_url(self):
        '''only allow logged in users '''
        return reverse("login")

    def get_queryset(self):
        """Limit deletion to entries belonging to lists owned by viewer."""
        query = super().get_queryset()
        viewer = Viewer.objects.get(user=self.request.user)
        return query.filter(listed__viewer=viewer)

    def get_success_url(self):
        '''return to list detail after form completes'''
        return reverse("list_detail", args=[self.object.listed.pk])

    
    






