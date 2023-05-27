from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer

# AUTH

@api_view(['POST'])
def signin(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        return Response({'token': token})
    else:
        return Response({'error': 'Credenciais inválidas.'}, status=400)


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# FOLLOW SYSTEM

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    request.user.following.add(user_to_follow)
    return Response({'status': 'success'}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    request.user.following.remove(user_to_unfollow)
    return Response({'status': 'success'}, status=200)