# project/models.py
# holds all the models for the project site
# Author: Mia Batista 


from django.db import models

# from django.urls import reverse

from django.contrib.auth.models import User 
# Create your models here.

class Viewer(models.Model):
    """Encapsulate the data of a user's profile"""

    # outline the data attributes of the Viewer
    # chose one to one field instead of ForeignKey unlike in mini_insta 
    # to handle/ensure only one viewer profile per Django user, avoiding duplicates 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(blank=True)

    def __str__(self):
        '''string representation of Viewer'''
        return f'{self.user} by {self.display_name}'
    

class Show(models.Model):
    '''Encapsulates a TV show'''

    STATUS_CHOICES = [
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("hiatus", "On Hiatus"),
    ]

    title = models.TextField(blank=True)
    description = models.TextField(blank=True)
    release_year = models.PositiveIntegerField()
    genre = models.TextField()
    status = models.CharField(
        choices=STATUS_CHOICES,
        default="ongoing",)
    poster_image = models.ImageField(blank=True)
    created_by = models.ForeignKey(Viewer,on_delete=models.CASCADE,related_name="created_shows",blank=True,null=True)


    def __str__(self):
        '''string representation of Viewer'''
        return f'{self.title}'
    

class Season(models.Model):
    """Encapsulates a specific season of a show."""
    
    show = models.ForeignKey(Show, on_delete=models.CASCADE,related_name="seasons")
    season_number = models.PositiveIntegerField()
    title = models.TextField(blank=True)

    # provides specifics when storing data in the database
    # ordering, done by show then season in that order 
    # unique together, prevents duplicates of multiple season 1's for one show
    class Meta:
        ordering = ["show", "season_number"]
        unique_together = ("show", "season_number")

    def __str__(self):
        # Fleabag - Season 1 is an example of the string representation 
        base = self.title or f"Season {self.season_number}"
        return f"{self.show.title} - {base}"
    
class Review(models.Model):
    '''Encapsultes the data for a review left by a profile'''

    viewer = models.ForeignKey(Viewer, on_delete=models.CASCADE, related_name="reviews")
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # makes sure its in the order of created at 
    class Meta:
        ordering = ['created_at']

        # might add the unique pairing of viewer and show 
    
    def __str__(self):
        """string representation of the Review model"""
        return f'Review of {self.show.title} by {self.viewer}'
    
class List(models.Model):
    '''encapsulates the data ffor the list of shows created by viewer'''

    viewer = models.ForeignKey(Viewer, on_delete=models.CASCADE, related_name="lists")
    title = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # makes sure its in the order of created at 
    class Meta:
        ordering = ['created_at']

    def __str__(self):
        """string representation of the List model"""
        return f'Review of {self.title} ({self.viewer})'
    
class ListEntry(models.Model):
    """encapsulates the relationship between Show and List to allow for ranking """
    
    listed = models.ForeignKey(List, on_delete=models.CASCADE, related_name="entries")
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name="list_entries")
    position = models.PositiveIntegerField(blank=True)


    # similar reasoning from other class for Meta 
    class Meta:
        ordering = ["position", "id"]
        unique_together = ("listed", "show")

    def __str__(self):
        '''string representation of the ListEntry Class'''
        return f"{self.show.title} in {self.listed.title}"

class Watch(models.Model):
    '''model that stores if a Viewer is watching or has finished a show'''
    
    STATUS_CHOICES = [
        ("W", "Watching"),
        ("F", "Finished"),
    ]

    viewer = models.ForeignKey(Viewer,on_delete=models.CASCADE,related_name="watches")
    show = models.ForeignKey(Show,on_delete=models.CASCADE,related_name="watches")
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,default="W")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("viewer", "show")

    def __str__(self):
        return f"{self.viewer.display_name} – {self.show.title} ({self.get_status_display()})"


