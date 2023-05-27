from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('<int:user_id>/follow/', views.follow, name='follow'),
    path('<int:user_id>/unfollow/', views.unfollow, name='unfollow'),
]
