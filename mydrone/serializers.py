''' Serialisers.py'''
# from django.contrib.auth.models import User, Group
from .models import Category, Drone
from rest_framework import serializers

class DroneSerializer(serializers.HyperlinkedModelSerializer):    
    category = serializers.CharField(source='category.id')    
    class Meta:
        model = Drone   
        fields = '__all__'

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    drones = DroneSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ('name') 