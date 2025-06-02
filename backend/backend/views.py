from django.http import FileResponse
import os
from django.conf import settings

from filesnew.models import Filesnew
from filesnew.serializers import FilesnewSerializer
from rest_framework.decorators import api_view


def serve_csv_inline(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)

    # Правильный content-type
    response = FileResponse(open(file_path, 'rb'), content_type='text/csv')

    # Заголовок файла в браузере
    response['Content-Disposition'] = f'inline; filename="{filename}"'

    return response

### Было норм
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os


@csrf_exempt  # Отключение проверки CSRF
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_path = os.path.join('media/uploads/', uploaded_file.name)

        with open(file_path, 'wb+') as f:
            for chunk in uploaded_file.chunks():
                f.write(chunk)

        return JsonResponse({'message': 'File uploaded successfully!', 'file_path': file_path})
    return JsonResponse({'error': 'No file uploaded'}, status=400)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.core.files.base import ContentFile
import base64

import os

## до этого было норм
# views.py
