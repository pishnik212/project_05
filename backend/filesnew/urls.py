from django.urls import path
from .views import FilesnewView, SaveEditedFile, upload_selected  # , AddFilesnewView

urlpatterns = [
    path('filesnews/',FilesnewView.as_view())
,path('filesnews/<int:pk>/', FilesnewView.as_view()),
path('filesnews/savefile/', SaveEditedFile.as_view(), name='save_edited_file'),
path('filesnews/upload-selected/', upload_selected, name='upload_selected'),
]
