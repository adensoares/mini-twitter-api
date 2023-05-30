from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Tweet
from .serializers import TweetSerializer

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            return Response({"error": "Not authenticated"}, status=403)

    @permission_classes([IsAuthenticated])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    @action(detail=False, methods=['get'])
    def general_feed(self, request):
        tweets = Tweet.objects.all()
        user = request.user
        if user.is_authenticated:
            # No feed, usuário não deve ver as próprias publicações
            tweets = tweets.exclude(user=user)
        tweets = tweets.order_by('-created_at')[:10]
        serializer = self.get_serializer(tweets, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['get'])
    @permission_classes([IsAuthenticated])
    def personal_feed(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({"error": "Not authenticated"}, status=403)
        followed_users = user.following.all()
        tweets = Tweet.objects.filter(user__in=followed_users).exclude(user=user).order_by('-created_at')[:10]
        serializer = self.get_serializer(tweets, many=True)
        return Response(serializer.data)
