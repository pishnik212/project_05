from django.urls import path
from .views import FacultyView

urlpatterns = [
    path('faculty/', FacultyView.as_view())
,path('faculty/<int:pk>/', FacultyView.as_view())
]
