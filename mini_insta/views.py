# mini_insta/views.py
# author: Mia Batista 
# views.py file that obtains all the data for the website
# general view allows general view formats that handle common instances  

from django.shortcuts import render
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView

from django.urls import reverse
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from .models import Profile, Post, Photo

from django.contrib.auth.mixins import LoginRequiredMixin ## NEW for auth

# Create your views here.

class ProfileRequiredMixin(LoginRequiredMixin):
    # Send users to our app's login URL, not /accounts/login/
    # My own subclass for the LoginRequiredMixin since a lot of classes need this 

    def get_login_url(self):
        return reverse('login')

    # Convenience: current logged-in user's Profile
    def get_current_profile(self):
        return Profile.objects.get(user=self.request.user)

class ProfileListView(ListView):
    '''Define a view class to obtain data for all Profile records'''
    # all instances that exist in the model, doesnt care about the pk 
    #  ListView
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    '''display a single profile'''

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

class PostDetailView(DetailView):
    '''displays a single post'''
    # detail view looks for a primary key
    # new instances of the model = CreateView  
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = 'post'

class CreatePostView(ProfileRequiredMixin, CreateView):
    '''A view to handle creation of a new Post
        1) display the HTML form to user (GET)
        2) process the form submission and store the new Post object (POST)
        '''

    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'


    def get_context_data(self, **kwargs):
        '''return the dictionary of context variaable for is in the template'''
        context = super().get_context_data(**kwargs)
        # pk = self.kwargs['pk']
        context['profile'] = self.get_current_profile()
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the new object to 
        the Django database. We need to add the foreign key (of the Profile) to 
        the Comment object before saving it to the database.'''

        me = self.get_current_profile()

        form.instance.profile = me

        post = form.save()
        post.save()
        
        fotos = self.request.FILES.getlist('files')
        for foto in fotos:
            photo = Photo()
            photo.image_file = foto
            photo.post = post
            photo.save()
            
        # delegate the work to the superclass method form_valid 
        response = super().form_valid(form)

        return response
    
    def get_success_url(self):
        '''after creating a post, return to the profile page'''
        user = self.get_current_profile()
        return reverse('show_profile', kwargs={'pk': user.pk})

class UpdateProfileView(ProfileRequiredMixin, UpdateView):
    '''A view to handle when a profile is updated'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_object(self):
        # always edit the logged-in user’s profile
        return self.get_current_profile()
    



class DeletePostView(ProfileRequiredMixin, DeleteView):
    '''A view to handle when a profile is updated'''
    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_queryset(self):
        """Limit deletion to posts owned by the logged-in user's profile."""
        query = super().get_queryset()
        return query.filter(profile=self.get_current_profile())

    
    def get_context_data(self, **kwargs):
        '''return the dictionary of context variable for is in the template'''

        # calling the superclass method 
        context = super().get_context_data(**kwargs)
        
        # setting the context variables 
        context['post'] = self.object
        context['profile'] = self.object.profile

        return context 

    def get_success_url(self):
        '''after deleting a post, return to the profile page'''
        pk = self.kwargs['pk']

        post = Post.objects.get(pk=pk)
        profile = post.profile
        return reverse('show_profile', kwargs={'pk': profile.pk})


class UpdatePostView(ProfileRequiredMixin, UpdateView):
    '''A view to handle when a profile is updated'''
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_queryset(self):
        """Limit deletion to posts owned by the logged-in user's profile."""
        query = super().get_queryset()
        return query.filter(profile=self.get_current_profile())
    
    def get_success_url(self):
        '''after updating a post, return to the profile page'''
        pk = self.kwargs['pk']
        return reverse('show_post', kwargs={'pk': pk})
    


class ShowFollowersDetailView(DetailView):
    '''provides the context variable profile to their templates to show followers'''
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    '''provides the context variable profile to their templates to show following'''
    
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class PostFeedListView(ProfileRequiredMixin, ListView):
    '''provides context variable to show the Post Feed as a List View'''

    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        '''helper method to retrieve the post feed using the method from profile'''
        query = self.get_current_profile()
        return query.get_post_feed()

    def get_context_data(self, **kwargs):
        '''return the dictionary of context variable for the data in the template'''
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_current_profile()
        return context
    
class SearchView(ProfileRequiredMixin, ListView):
    '''searches profiles and posts'''
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        '''used to dispatch/handle any request'''

        self.profile = self.get_current_profile()
        q = self.request.GET.get('query', '').strip()
        if not q:
            return render(request, 'mini_insta/search.html', {'profile': self.profile})
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        '''method to obtain the QuesrySet of instance data'''
        q = self.request.GET.get('query', '').strip()
        if not q:
            return Post.objects.none()
        return Post.objects.filter(caption__icontains=q).order_by('-timestamp')
    
    def get_context_data(self, **kwargs):
        '''return the dictionary of context data that can be accessed from the template'''
        context = super().get_context_data(**kwargs)

        q = self.request.GET.get('query', '').strip()   
        if q:
            profiles = (
                Profile.objects.filter(username__icontains=q) |
                Profile.objects.filter(display_name__icontains=q) |
                Profile.objects.filter(bio_text__icontains=q)
            ).distinct().order_by('username')
        else:
            profiles = Profile.objects.none()

        context['profile'] = self.profile          
        context['query'] = q
        context['profiles'] = profiles
        return context


class MyProfileDetailView(ProfileRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        """Return the logged-in user's own Profile."""
        return Profile.objects.get(user=self.request.user)
