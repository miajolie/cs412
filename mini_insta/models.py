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