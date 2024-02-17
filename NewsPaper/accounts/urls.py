from django.urls import path
from .views import SignUp, ProfileUser, set_timezone

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    path('set_timezone/', set_timezone, name='set_timezone'),
]