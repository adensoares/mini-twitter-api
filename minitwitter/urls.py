from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet
from tweets.views import TweetViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tweets', TweetViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/users/', include('users.urls')),
    path('api/v1/tweets/', include('tweets.urls')),
]
