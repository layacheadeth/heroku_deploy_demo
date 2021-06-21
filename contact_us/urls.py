from django.urls import path
from .views import *


urlpatterns = [
    path('contact_us/<int:pk>/',ContactUs_detail),
    path('contact_us/',ContactUs_view),
]