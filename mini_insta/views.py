# views.py file that obtains all the data for the website 

from django.shortcuts import render
from django.views.generic import ListView,DetailView, CreateView

from django.urls import reverse
from .forms import CreatePostForm
from .models import Profile, Post, Photo

# Create your views here.

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

class CreatePostView(CreateView):
    '''A view to handle creation of a new Post
        1) display the HTML form to user (GET)
        2) process the form submission and store the new Post object (POST)
        '''

    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self, **kwargs):
        '''return the dictionary of context variaable for is in the template'''
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['profile'] = Profile.objects.get(pk=pk)
        return context
    
    def form_valid(self, form):
        '''This method handles the form submission and saves the new object to 
        the Django database. We need to add the foreign key (of the Profile) to 
        the Comment object before saving it to the database.'''

        # retrive the pj from the url pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # set the fk 
        form.instance.profile = profile

        post = form.save()
        post.save()


        # handles when the user input the image_url for the form
        if not self.request.POST.get('image_url'):
            return super().form_valid(form)
        
        # creating photo object for url input
        photo = Photo()
        photo.image_url = self.request.POST.get('image_url')
        photo.post = post
        photo.save()

        # delegate the work to the superclass method form_valid 
        response = super().form_valid(form)

        return response
    
    def get_success_url(self):
        '''after creating a post, return to the profile page'''
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': pk})


