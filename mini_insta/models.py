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
    

class Post(models.Model):
    '''will model the data attributes of an Instagram post'''

    profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    # every Post object is related to a single Profile object
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True) 

    def __str__(self):
        '''returns a string representation of the model instance '''
        return f'{self.caption} belonging to {self.profile}'

class Photo(models.Model):
    '''will model the data attributes of an image associated with a Post'''

    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    # every Photo object is related to a single Post object
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str___(self):
        '''return a string representation of the model instance'''
        return f'{self.image_url} belonging to {self.post}'


