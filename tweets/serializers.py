from rest_framework import serializers
from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.full_name', read_only=True)
    userId = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'user', 'userId', 'content', 'created_at']
