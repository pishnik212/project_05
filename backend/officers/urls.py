from django.urls import path
from .views import OfficerView
from . import views

urlpatterns = [
    path('officers/',OfficerView.as_view())
,path('officers/<int:pk>/', OfficerView.as_view())
    , path('officers/officer-by-user/<int:user_id>/', views.get_officer_by_user_id, name='get_officer_by_user_id'),

]

