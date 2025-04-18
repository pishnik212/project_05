from django.urls import path
from .views import UniversityView

urlpatterns = [
    path('university/', UniversityView.as_view())
,path('university/<int:pk>/', UniversityView.as_view())
]
