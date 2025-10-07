# the Profile model and its attributes for an individual user
from django.db import models


# Create your models here.
class Profile(models.Model):
    '''Encapsulate the data of a blog Profile by an Individual User'''

    #define the data attributes of the Article object
    username = models.TextField(blank=True)
    display_name = models.TextField(blank=True)
    bio_text = models.TextField(blank=True)
    profile_image_url = models.URLField(blank=True)
    join_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        '''returns a string representation of the model instance '''
        return f'{self.username} by {self.display_name}'
    
    def get_all_posts(self):
        '''Return a QuerySet of posts from a profile'''
        # object method 
        posts = Post.objects.filter(profile = self)
        # list method = no need for the objects method
        post = posts.order_by("-timestamp")
        return post

class Post(models.Model):
    '''will model the data attributes of an Instagram post'''

    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    # every Post object is related to a single Profile object
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True) 

    def __str__(self):
        '''returns a string representation of the model instance '''
        return f'{self.caption} belonging to {self.profile}'
    
    def get_all_photos(self):
        '''Return a QuerySet of photos for a given post'''
        return Photo.objects.filter(post = self)



class Photo(models.Model):
    '''will model the data attributes of an image associated with a Post'''

    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    # every Photo object is related to a single Post object
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True)


    def __str__(self):
        '''return a string representation of the model instance'''
        # return f'{self.image_url} belonging to {self.post}' old method
        if self.image_file:
            return f'{self.image_file} belonging to {self.post}'
        if self.image_url:
            return f'{self.image_url} belonging to {self.post}'
        else:
            return "No Image"


    
    def get_image_url(self):
        '''fetches the proper image, decides between url and file url'''
        if self.image_url:
            return self.image_url
        elif self.image_file:
            return self.image_file.url
             
        return ''


