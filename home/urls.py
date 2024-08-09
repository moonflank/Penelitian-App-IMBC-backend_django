# urls.py

from django.urls import path
from .views import user_info

urlpatterns = [
    path('user-info/', user_info, name='user_info'),
]
