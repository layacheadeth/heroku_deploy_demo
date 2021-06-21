from django.urls import  path
from .views import *
urlpatterns=[
    path('users/register',RegisterView.as_view()),
    path('users/login',LoginView.as_view()),
    path('users/User',UserView.as_view()),
    path('users/logout',LogoutView.as_view()),
]