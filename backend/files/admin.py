from django.contrib import admin
from .models import File

models_list = [File]
admin.site.register(models_list)