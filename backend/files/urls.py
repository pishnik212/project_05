from django.urls import path
from .views import FileView

urlpatterns = [
    path('files/',FileView.as_view())
,path('files/<int:pk>/', FileView.as_view())
]
