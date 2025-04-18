from django.contrib import admin
from .models import Officer

models_list = [Officer]
admin.site.register(models_list)