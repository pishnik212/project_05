from django.urls import path

from .views import PredictfileView


urlpatterns = [
    path('predictfile/', PredictfileView.as_view(), name='predictfile-list'),  # Для списка и создания
    path('predictfile/<int:pk>/', PredictfileView.as_view(), name='predictfile-detail'),  # Для получения, обновления и удаления
    path('predictfile/<int:pk>/download/', PredictfileView.as_view()),  # Для получения, обновления и удаления
]