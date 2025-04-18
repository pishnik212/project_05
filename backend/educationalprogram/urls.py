from django.urls import path
from .views import EducationalprogramView

urlpatterns = [
    path('educationalprogram/', EducationalprogramView.as_view())
,path('educationalprogram/<int:pk>/', EducationalprogramView.as_view())
]
