from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .serializers import FilesnewSerializer
from django.core.files.storage import FileSystemStorage
from model_code.model_use import merge_excel_files


class FilesnewView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_filesnew(self, pk):
        try:
            return Filesnew.objects.get(fileId=pk)  # Исправлено на fileId
        except Filesnew.DoesNotExist:
            return None  # Возвращаем None, если файл не найден

    def put(self, request, pk=None):
        filesnew = self.get_filesnew(pk)
        if not filesnew:
            return JsonResponse({"message": "Файл не существует."}, status=404)

        incoming_data = request.data.copy()

        # Если файл пришёл — обновляем, иначе оставляем старый
        if 'Filesnew' not in request.FILES:
            incoming_data['Filesnew'] = filesnew.Filesnew

        serializer = FilesnewCreateSerializer(filesnew, data=incoming_data, partial=True)

        # было норм
        # serializer = FilesnewSerializer(filesnew, data=incoming_data, partial=True)

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
        print("FILES:", request.FILES)  # ← добавь это
        print("DATA:", request.data)

        serializer = FilesnewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # подставляем вручную
            return Response({'message': 'Файл успешно добавлен!'})
        return Response(serializer.errors, status=400)

    def get(self, request, pk=None):
        if pk:
            filesnew = self.get_filesnew(pk)
            serializer = FilesnewSerializer(filesnew)
        else:
            filesnews = Filesnew.objects.all()
            serializer = FilesnewSerializer(filesnews, many=True)
        return Response(serializer.data)

    def delete(self, request, pk=None):
        filesnew = self.get_filesnew(pk)
        filesnew.delete()
        return JsonResponse("Файл успешно удален!", safe=False)

    def update_file_only(request, pk=None, self=None):
        # Получаем объект Filesnew по pk
        filesnew = self.get_filesnew(pk)
        if not filesnew:
            return JsonResponse({"message": "Файл не существует."}, status=404)

        # Проверяем, передан ли новый файл
        if 'Filesnew' not in request.FILES:
            return JsonResponse({"message": "Файл не существует."}, status=400)

        # Получаем новый файл из запроса
        new_file = request.FILES['Filesnew']
        file_path = os.path.join('media/uploads', new_file.name)  # Путь для сохранения нового файла

        # Открываем новый файл для записи
        with open(file_path, 'wb+') as f:
            for chunk in new_file.chunks():
                f.write(chunk)

        # Обновляем поле Filesnew на новый путь к файлу
        filesnew.Filesnew = file_path

        # Сохраняем изменения в модели (оставшиеся поля не меняются)
        filesnew.save()

        return JsonResponse({
            "message": "Файл успешно обновлен!",
            "data": {
                "fileId": filesnew.fileId,
                "Filesnew": filesnew.Filesnew,
                "Name": filesnew.Name,
                "DownloadDate": filesnew.DownloadDate,
                "AdmissionYear": filesnew.AdmissionYear,
                "DownloadOfficerId": filesnew.DownloadOfficerId,
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
            return JsonResponse({"message": "Файл не загружен"}, status=400)

        print('Ищем в БД')
        # Находим файл в базе данных
        try:
            file_record = Filesnew.objects.get(id=file_id)
        except Filesnew.DoesNotExist:
            return JsonResponse({"message": "File not found in the database"}, status=404)

        # Сохраняем новый файл на сервере
        fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'uploads'))
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        # Обновляем путь к файлу в базе данных
        file_record.Filesnew = file_url  # Обновляем поле с файлом
        file_record.save()

        return JsonResponse({
            "message": "Файл успешно обновлен!!",
            "file_url": file_url
        })

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from officers.models import Officer


@method_decorator(csrf_exempt, name='dispatch')
class SaveEditedFile(View):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        print("FILES:", request.FILES)
        print("DATA:", request.data)

        try:
            user = request.user
            officer = Officer.objects.get(user=user)  # ищем офицера по текущему юзеру
            print(officer)
        except Officer.DoesNotExist:
            return Response({'error': 'Officer not found for this user'}, status=404)

        serializer = FilesnewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(DownloadOfficerId=officer)  # подставляем вручную
            return Response({'message': 'Файл успешно добавлен!'})
        return Response(serializer.errors, status=400)

    def save_edited_file(request):
        file_id = request.GET.get('id')
        uploaded_file = request.FILES.get('file')

        if not file_id or not uploaded_file:
            return JsonResponse({"message": "Missing file ID or file."}, status=400)

        try:
            file_record = Filesnew.objects.get(id=file_id)

            # Удаляем старый файл, если он существует
            if file_record.Filesnew and os.path.exists(file_record.Filesnew.path):
                os.remove(file_record.Filesnew.path)
                print('Удалили старый файл')

            # Сохраняем новый файл
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # Используем MEDIA_ROOT
            print(settings.MEDIA_ROOT)
            filename = fs.save(uploaded_file.name, uploaded_file)  # Сохраняем в MEDIA_ROOT
            print(filename)
            file_record.Filesnew = os.path.join('uploads', filename)  # Сохраняем относительный путь, без MEDIA_URL

            file_record.save()

            return JsonResponse({
                "message": "Файл успешно обновлен!!",
                "file_url": file_record.Filesnew
            }, status=200)

        except Filesnew.DoesNotExist:
            return JsonResponse({"message": "Файл не обнаружен."}, status=404)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Filesnew
from .serializers import FilesnewCreateSerializer
class FilesnewCreateView(APIView):
    def post(self, request):
        serializer = FilesnewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Файл успешно добавлен!'})
        return Response(serializer.errors, status=400)


from filesnew.models import Filesnew
from django.http import JsonResponse
from .models import Filesnew
from emptyfile.models import Emptyfile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now
import os
from django.conf import settings  # для доступа к MEDIA_ROOT


@api_view(['POST'])
def upload_selected(request):
    number = int(request.data.get('number', 0))
    selected_ids_raw = request.data.get('selectedIds', '')
    empty_selected_ids_raw = request.data.get('emptySelectedIds', '')
    print('values01', selected_ids_raw, empty_selected_ids_raw)

    # Преобразуем строки в списки чисел
    try:
        selected_ids = list(map(int, selected_ids_raw.split('_'))) if selected_ids_raw else []
        empty_selected_ids = list(map(int, empty_selected_ids_raw.split('_'))) if empty_selected_ids_raw else []
    except ValueError:
        return Response({'error': 'ID должны быть числами, разделёнными "_"'}, status=400)

    if number <= 0 or not selected_ids or not empty_selected_ids:
        return Response({'error': 'Нужно выбрать хотя бы по одному файлу из каждого списка и ввести число'}, status=400)

    # Составляем список путей к файлам
    files_paths, empty_files_paths = [], []

    for file_obj in Filesnew.objects.filter(fileId__in=selected_ids):
        files_paths.append(file_obj.Filesnew.path)

    for file_obj in Emptyfile.objects.filter(fileId__in=empty_selected_ids):
        empty_files_paths.append(file_obj.Emptyfile.path)

    if not files_paths:
        return Response({'error': 'Нет файлов для объединения'}, status=400)

    if not empty_files_paths:
        return Response({'error': 'Нет файлов для прогнозирования'}, status=400)

    print('вызываем функцию объединения файлов', files_paths, empty_files_paths, number)
    # 👇 вызываем функцию объединения файлов
    try:
        result_df, total_rows = merge_excel_files(files_paths, empty_files_paths,
                                                  number)  # передаем number и получаем количество строк
    except Exception as e:
        return Response({'error': f'Ошибка при объединении файлов: {e}'}, status=500)

    print('total_rows', total_rows)
    # Генерация имени файла
    timestamp = now().strftime("%Y%m%d_%H%M%S")
    file_name = f"prediction_{timestamp}_{'_'.join(map(str, selected_ids))}__{'_'.join(map(str, empty_selected_ids))}.xlsx"
    relative_file_path = os.path.join('predictions', file_name)
    abs_file_path = os.path.join(settings.MEDIA_ROOT, relative_file_path)

    os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)  # если папки нет — создаём

    result_df.to_excel(abs_file_path, index=False)

    return Response({
        'message': 'Файл создан и сохранён',
        'fileUrl': f'/media/{relative_file_path}',
        'minExamScore': total_rows  # Добавляем число
    })
