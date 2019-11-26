from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from .views import TokenAuthView,SignUpView
urlpatterns = [
    path('login/', ObtainAuthToken.as_view, name='api_login'), 
    path('auth/', TokenAuthView.as_view(), name='api_auth'),
    path('signup/', SignUpView.as_view(), name='api_signup'),
]
