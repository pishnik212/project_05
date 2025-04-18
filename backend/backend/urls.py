from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from .views import upload_selected

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('officers.urls')),
    path('', include('files.urls')),
    path('', include('filesnew.urls')),
path('', include('university.urls')),
# path('filesnews/upload-selected/', upload_selected),
path('', include('predictfile.urls')),
path('', include('emptyfile.urls')),
path('', include('user.urls')),
path('', include('educationalprogram.urls')),
path('', include('educationform.urls')),
path('', include('faculty.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
