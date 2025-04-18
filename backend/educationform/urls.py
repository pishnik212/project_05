from django.urls import path
from .views import EducationformView

urlpatterns = [
    path('educationform/', EducationformView.as_view())
,path('educationform/<int:pk>/', EducationformView.as_view())
]
