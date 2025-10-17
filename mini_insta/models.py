# the Profile model and its attributes for an individual user
from django.db import models
from django.urls import reverse

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
    
    def get_absolute_url(self):
        '''Return a URL to display one instance of this object'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_followers(self):
        '''returns a ilst of Profiles who follow this profile'''
        query = Follow.objects.filter(profile=self)
        # selects those connected by an edge / connected to one another 
        return [f.follower_profile for f in query]
    
    def get_num_followers(self):
        '''returns the number of followers'''
        return Follow.objects.filter(profile=self).count()
    
    def get_following(self):
        '''return list of profiles this profile follows'''

        # query = Follow.objects.filter(follower_profile=self).select_related('profile')
        query = Follow.objects.filter(follower_profile=self)
        return [f.profile for f in query]
    
    def get_num_following(self):
        '''return count of how many profiles are being follwed'''
        return Follow.objects.filter(follower_profile=self).count()
    
    def get_post_feed(self):
        '''returns a queryset of posts'''
        following = self.get_following()
        return Post.objects.filter(profile__in = following).order_by('-timestamp')

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

    def get_all_comments(self):
        '''return a QuerySet of all comments on a post'''
        return Comment.objects.filter(post = self)
    
    def get_likes(self):
        '''retrieves all likes on a post'''
        return Like.objects.filter(post=self)
    
    def get_num_likes(self):
        '''helper method to get the number of likes'''
        return self.get_likes().count()


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


class Follow(models.Model):
    '''encapsulates the idea of a profile connecting to another profile'''

    profile = models.ForeignKey('Profile', on_delete = models.CASCADE, related_name= 'profile')
    follower_profile = models.ForeignKey('Profile', on_delete = models.CASCADE, related_name= 'follower_profile')

    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''string method for the Follow class'''
        return f"{self.follower_profile.display_name} follows {self.profile.display_name}"
    
class Comment(models.Model):
    '''a comment by a Profile on a Post'''
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self):
        '''string representation of the comment class'''
        person = self.profile.display_name or self.profile.username
        return f"Comment by {person} on Post #{self.post.pk}: {self.text}..."

class Like(models.Model):
    '''encapsulates the idea of a profile "liking" a post'''
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''string representation of the like class'''
        person = self.profile.display_name or self.profile.username
        return f"{person} liked Post #{self.post.pk}"
    



