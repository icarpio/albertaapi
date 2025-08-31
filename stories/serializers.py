from rest_framework import serializers
from .models import Story, HorrorStory

class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'

class HorrorStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HorrorStory
        fields = ['id', 'title', 'content', 'created_at']