
from django.urls import path

from .views import login_view

urlpatterns = [
path('user/login/', login_view, name='login'),
]

