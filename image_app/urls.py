# image_app/urls.py

from django.urls import path
from .views import fetch_image, home

urlpatterns = [
    path('', home, name='home'),
    path('image/fetch_image/', fetch_image, name='fetch_image'),
]

