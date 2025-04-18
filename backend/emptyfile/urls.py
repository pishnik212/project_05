from django.urls import path
from .views import EmptyfileView, SaveEditedFile, upload_selected  # , AddFilesnewView

urlpatterns = [
    path('emptyfile/',EmptyfileView.as_view())
,path('emptyfile/<int:pk>/',EmptyfileView.as_view()),
path('emptyfile/savefile/', SaveEditedFile.as_view(), name='save_edited_file'),
path('emptyfile/upload-selected/', upload_selected, name='upload_selected'),
]
