from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from .models import Predictfile
from .serializers import PredictfileSerializer
from rest_framework.decorators import action
from rest_framework import permissions

from filesnew.models import Filesnew
from django.http import FileResponse
from django.utils.encoding import smart_str

class PredictfileView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, *args, **kwargs):
        # Получение списка всех Predictfile
        predictfiles = Predictfile.objects.all()
        serializer = PredictfileSerializer(predictfiles, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        import math
        data = request.data.copy()  # Создаем копию, чтобы можно было редактировать

        # Безопасная обработка MinExamScore
        min_score = data.get('MinExamScore', 0)
        print('min_score1', min_score)

        try:
            min_score = float(min_score)
            if math.isnan(min_score) or math.isinf(min_score):
                min_score = 0
        except (ValueError, TypeError):
            min_score = 0

        data['MinExamScore'] = min_score  # Обновляем значение
        print('min_score2', min_score)

        serializer = PredictfileSerializer(data=data)

        if serializer.is_valid():
            predictfile = serializer.save()

            # Получаем список SourceFiles и фильтруем только корректные числовые значения
            raw_ids = request.data.getlist('SourceFiles')
            print('raw_ids', raw_ids)
            valid_ids = []

            for file_id in raw_ids:
                try:
                    int_id = int(file_id)
                    valid_ids.append(int_id)
                except (ValueError, TypeError):
                    # Просто пропускаем некорректные id
                    continue
            print('ok111')

            if not valid_ids:
                print("Serializer errors:", serializer.errors)

                return Response({'error': 'Не передано ни одного корректного ID файла.'},
                                status=status.HTTP_400_BAD_REQUEST)
            print('ok222')
            # Добавляем файлы в связь
            for file_id in valid_ids:
                try:
                    # Попробуем безопасно преобразовать в int
                    file_id = int(file_id)
                    file_instance = Filesnew.objects.get(fileId=file_id)
                    predictfile.SourceFiles.add(file_instance)
                except (ValueError, TypeError):
                    return Response({'error': f'Некорректный ID файла: {file_id}'}, status=status.HTTP_400_BAD_REQUEST)
                except Filesnew.DoesNotExist:
                    return Response({'error': f'Файл с id {file_id} не существует'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('ok333')
        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return Predictfile.objects.get(pk=pk)
        except Predictfile.DoesNotExist:
            return None

    def retrieve(self, request, pk=None):
        # Получение конкретного Predictfile
        predictfile = self.get_object(pk)
        if predictfile:
            serializer = PredictfileSerializer(predictfile)
            return Response(serializer.data)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk=None):
        # Обновление Predictfile
        predictfile = self.get_object(pk)
        if predictfile:
            serializer = PredictfileSerializer(predictfile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        # Удаление Predictfile
        predictfile = self.get_object(pk)
        if predictfile:
            predictfile.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def download_file(request, file_id):
        file_obj = get_object_or_404(Predictfile, pk=file_id)
        response = FileResponse(file_obj.PredictedFile.open(), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{smart_str(file_obj.PredictedFile.name)}"'
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return response
