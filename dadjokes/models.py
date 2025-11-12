# dadjokes/models.py


from django.db import models

# Create your models here.

class Joke(models.Model):
    '''Encapsulate the data of a dadjoke joke'''
    text = models.TextField(blank=True)
    name = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True) 

    def __str__(self):
        '''returns a string representation of the model instance '''
        return f'{self.name} = {self.text}'

class Picture (models.Model):
    '''Encapsulate the data of a picture'''

    image_url = models.URLField(blank=True)
    name = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True) 

    def __str__(self):
        '''returns a string representation of the model instance '''
        return f'{self.name}'