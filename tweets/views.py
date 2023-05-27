from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Tweet
from .serializers import TweetSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_tweet(request):
    serializer = TweetSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def general_feed(request):
    tweets = Tweet.objects.order_by('-created_at')[:10]
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def personalized_feed(request):
    user = request.user
    followed_users = user.following.all()  # Assuming you have a related_name='following' in the User model
    tweets = Tweet.objects.filter(user__in=followed_users).order_by('-created_at')[:10]
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)
