from django.db import models
from django.urls import reverse

# Create your models here.
class Article(models.Model):
    '''Encapsulate the data of a blog Article by an Author'''

    #define the data attributes of the Article object
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''returns a string representation of the model instance '''
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        '''Return a URL to display one instance of this object'''

        return reverse('article', kwargs={'pk': self.pk})
    def get_all_comments(self):
        '''Return a QuerySet of comments abiyt this article'''
        # looking for comments are of the instance of this comment "self"
        comments = Comment.objects.filter(article = self)
        return comments

    
class Comment(models.Model):
    '''encapsulte the idea of a comment about an Article'''

    article = models.ForeignKey(Article, on_delete = models.CASCADE)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now=True) 

    def __str__(self):
        '''returns a string representation of the model instance '''
        return f'{self.text}'
