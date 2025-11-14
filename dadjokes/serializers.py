# dadjokes/serializers.py
# Serializers convert our django data models to a 
# text-representation suitable to transmit over HTTP.
# Mia Jolie Batista 

from rest_framework import serializers
from .models import *
 
class JokeSerializer(serializers.ModelSerializer):
  '''
  A serializer for the Joke model.
  Specify which model/fields to send in the API.
  '''
 
  class Meta:
    model = Joke
    fields = ['id','text', 'name', 'timestamp']
   
  # add methods to customize the Create/Read/Update/Delete operations
#   might not need thus method?
  def create(self, validated_data):
    '''
    Override the superclass method that handles object creation.
    '''
    print(f'JokeSerializer.create, validated_data={validated_data}.')
 
    return Joke.objects.create(**validated_data)
  
class PictureSerializer(serializers.ModelSerializer):
  '''
  A serializer for the Picture model.
  Specify which model/fields to send in the API.
  '''
 
  class Meta:
    model = Picture
    fields = ['id', 'image_url', 'name', 'timestamp']
   
  # add methods to customize the Create/Read/Update/Delete operations
  def create(self, validated_data):
    '''
    Override the superclass method that handles object creation.
    '''
    print(f'PictureSerializer.create, validated_data={validated_data}.')
 
    return Picture.objects.create(**validated_data)

 