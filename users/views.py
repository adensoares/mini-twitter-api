from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer

class UserViewSet(mixins.CreateModelMixin, 
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=['get'])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


   
    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @permission_classes([IsAuthenticated])
    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        return self._toggle_follow(request, pk, action="follow")

    @permission_classes([IsAuthenticated])
    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        return self._toggle_follow(request, pk, action="unfollow")

    def _toggle_follow(self, request, pk, action):
        target_user = get_object_or_404(User, pk=pk)
        user = request.user
        if action == "follow":
            user.following.add(target_user)
        else:
            user.following.remove(target_user)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @permission_classes([IsAuthenticated])
    @action(detail=False, methods=['get'])
    def following(self, request):
        following_users = request.user.following.all()
        serializer = UserSerializer(following_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)