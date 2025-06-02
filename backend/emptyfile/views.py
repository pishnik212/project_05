from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import EmptyfileSerializer
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class EmptyfileView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_emptyfile(self, pk):
        try:
            return Emptyfile.objects.get(fileId=pk)  # Исправлено на fileId
        except Emptyfile.DoesNotExist:
            return None  # Возвращаем None, если файл не найден

    def put(self, request, pk=None):
        emptyfile = self.get_emptyfile(pk)
        if not emptyfile:
            return JsonResponse({"message": "Указанный файл не существует."}, status=404)

        incoming_data = request.data.copy()

        # Если файл пришёл — обновляем, иначе оставляем старый
        if 'Emptyfile' not in request.FILES:
            incoming_data['Emptyfile'] = emptyfile.Emptyfile

        serializer = EmptyfileCreateSerializer(emptyfile, data=incoming_data, partial=True)

        # было норм
        # serializer = EmptyfileSerializer(emptyfile, data=incoming_data, partial=True)

        if serializer.is_valid():
            print("Serializer validated data:", serializer.validated_data)
            serializer.save()
            print("FILES:", request.FILES)
            print("DATA:", request.data)
            return JsonResponse({
                "message": "Файл успешно обновлен!",
                "data": serializer.data
            }, status=200)
        else:
            print("FILES:", request.FILES)
            print("DATA:", request.data)
            return JsonResponse({
                "message": "Не удалось обновить файл.",
                "errors": serializer.errors
            }, status=400)


    def post(self, request):
        print("FILES:", request.FILES)  
        print("DATA:", request.data)
        serializer = EmptyfileCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Файл успешно добавлен!'})
        return Response(serializer.errors, status=400)


    def get(self, request, pk=None):
        if pk:
            emptyfile = self.get_emptyfile(pk)
            serializer = EmptyfileSerializer(emptyfile)
        else:
            emptyfiles = Emptyfile.objects.all()
            serializer = EmptyfileSerializer(emptyfiles, many=True)
        return Response(serializer.data)



    def delete(self, request, pk=None):
        emptyfile = self.get_emptyfile(pk)
        emptyfile.delete()
        return JsonResponse("Файл успешно удален.", safe=False)

    def update_file_only(request, pk=None, self=None):
        # Получаем объект Emptyfile по pk
        emptyfile = self.get_emptyfile(pk)
        if not emptyfile:
            return JsonResponse({"message": "Файл не существует."}, status=404)

        # Проверяем, передан ли новый файл
        if 'Emptyfile' not in request.FILES:
            return JsonResponse({"message": "Файл не передан."}, status=400)

        # Получаем новый файл из запроса
        new_file = request.FILES['Emptyfile']
        file_path = os.path.join('media/uploads', new_file.name)  # Путь для сохранения нового файла

        # Открываем новый файл для записи
        with open(file_path, 'wb+') as f:
            for chunk in new_file.chunks():
                f.write(chunk)

        # Обновляем поле Emptyfile на новый путь к файлу
        emptyfile.Emptyfile = file_path

        # Сохраняем изменения в модели (оставшиеся поля не меняются)
        emptyfile.save()

        return JsonResponse({
            "message": "Файл успешно обновлен!",
            "data": {
                "fileId": emptyfile.fileId,
                "Emptyfile": emptyfile.Emptyfile,
                "Name": emptyfile.Name,
                "DownloadDate": emptyfile.DownloadDate,
                "AdmissionYear": emptyfile.AdmissionYear,
                "DownloadOfficerId": emptyfile.DownloadOfficerId,
            }
        }, status=200)

    # было норм ДО
    def save_edited_file(request):
        # Получаем параметры из URL
        file_id = request.GET.get('id')
        if not file_id:
            return JsonResponse({"message": "Отсутствует ID файла"}, status=400)

        # Проверяем, был ли загружен новый файл
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return JsonResponse({"message": "Файл не загружен."}, status=400)

        # Находим файл в базе данных
        try:
            file_record = Emptyfile.objects.get(id=file_id)
        except Emptyfile.DoesNotExist:
            return JsonResponse({"message": "Файл не найден в базе данных."}, status=404)

        # Сохраняем новый файл на сервере
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        # Обновляем путь к файлу в базе данных
        file_record.Emptyfile = file_url  # Обновляем поле с файлом
        file_record.save()

        return JsonResponse({
            "message": "Файл успешно обновлен!",
            "file_url": file_url
        })

from django.views import View
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class SaveEditedFile(View):
    def post(self, request):
        file_id = request.GET.get("id")
        uploaded_file = request.FILES.get("file")

        if not file_id or not uploaded_file:
            return JsonResponse({"error": "Недостаточно данных"}, status=400)

        try:
            # Находим объект по ID
            file_record = get_object_or_404(Emptyfile, pk=file_id)

            # Если файл существует, удаляем старый
            if file_record.Emptyfile and default_storage.exists(file_record.Emptyfile.name):
                default_storage.delete(file_record.Emptyfile.name)

            # Сохраняем новый файл
            file_path = default_storage.save(uploaded_file.name, uploaded_file)
            file_url = default_storage.url(file_path)  # Получаем полный URL с media/

            # Убираем часть '/media/' из пути, чтобы остался только относительный путь
            relative_file_url = file_url.replace(f'{settings.MEDIA_URL}', '')

            # Обновляем запись в базе данных
            file_record.Emptyfile = relative_file_url
            file_record.DownloadDate = timezone.now()  # если нужно обновить дату
            file_record.save()

            return JsonResponse({"status": "ok", "file_url": relative_file_url}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def save_edited_file(request):
        file_id = request.GET.get('id')
        uploaded_file = request.FILES.get('file')

        if not file_id or not uploaded_file:
            return JsonResponse({"message": "Недостаточно данных."}, status=400)

        try:
            file_record = Emptyfile.objects.get(id=file_id)

            # Удаляем старый файл, если он существует
            if file_record.Emptyfile and os.path.exists(file_record.Emptyfile.path):
                os.remove(file_record.Emptyfile.path)

            # Сохраняем новый файл
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # Используем MEDIA_ROOT
            filename = fs.save(uploaded_file.name, uploaded_file)  # Сохраняем в MEDIA_ROOT
            file_record.Emptyfile = os.path.join('uploads', filename)  # Сохраняем относительный путь, без MEDIA_URL

            file_record.save()

            return JsonResponse({
                "message": "Файл успешно обновлен!",
                "file_url": file_record.Emptyfile
            }, status=200)

        except Emptyfile.DoesNotExist:
            return JsonResponse({"message": "Файл не обнаружен."}, status=404)


# до было норм
from rest_framework.views import APIView
from .serializers import EmptyfileCreateSerializer

class EmptyfileCreateView(APIView):
    def post(self, request):
        serializer = EmptyfileCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Файл успешно добавлен!'})
        return Response(serializer.errors, status=400)


from emptyfile.models import Emptyfile  # заменить на актуальное имя модели
from django.http import JsonResponse
from django.utils.timezone import now
import pandas as pd
import os
from .models import Emptyfile
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def upload_selected(request):
    number = int(request.data.get('number', 0))
    selected_ids_raw = request.data.get('selectedIds', '')

    print(selected_ids_raw)


    # Если пришла строка — разбиваем её в массив чисел
    if isinstance(selected_ids_raw, str):
        try:
            selected_ids = list(map(int, selected_ids_raw.split('_')))
        except ValueError:
            return Response({'error': 'selectedIds должен содержать только числа, разделённые "_"'}, status=400)
    else:
        return Response({'error': 'selectedIds должен быть строкой'}, status=400)

    print(selected_ids)

    if number <= 0 or not selected_ids:
        return Response({'error': 'Invalid input'}, status=400)

    combined_data = []

    for file_obj in Emptyfile.objects.filter(fileId__in=selected_ids):
        file_path = file_obj.Emptyfile.path
        try:
            df = pd.read_excel(file_path)
            combined_data.append(df.head(number))  # Вытаскиваем только нужное количество строк
        except Exception as e:
            print(f"Ошибка чтения файла {file_path}: {e}")

    if not combined_data:
        return Response({'error': 'Нет данных для объединения'}, status=400)

    result_df = pd.concat(combined_data, ignore_index=True)

    # Генерация уникального имени файла
    timestamp = now().strftime("%Y%m%d_%H%M%S")
    file_name = f"prediction_{timestamp}_{'_'.join(map(str, selected_ids))}.xlsx"

    # Путь для сохранения файла
    file_path = os.path.join('predictions', file_name)
    abs_file_path = os.path.join('media', file_path)

    # Сохраняем результат
    result_df.to_excel(abs_file_path, index=False)

    return Response({
        'message': 'Файл создан и сохранен',
        'fileUrl': f'/media/{file_path}',
    })

