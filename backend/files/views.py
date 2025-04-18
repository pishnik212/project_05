from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import JsonResponse
from .models import File
from .serializers import FileSerializer


class FileView(APIView):

    def post(self, request):
        data = request.data
        serializer = FileSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Файл успешно добавлен!",          safe=False)
        return JsonResponse("Failed to Add File", safe=False)


    def get_file(self, pk):
        try:
            file = File.objects.get(fileId=pk)
            return file
        except:
            return JsonResponse("File Does Not Exist", safe=False)

    def get(self, request, pk=None):
        if pk:
            data = self.get_file(pk)
            serializer = FileSerializer(data)
        else:
            data = File.objects.all()
            serializer = FileSerializer(data, many=True)
        return Response(serializer.data)


    def put(self, request, pk=None):
        file_to_update = File.objects.get(fileId=pk)
        serializer = FileSerializer(instance=file_to_update, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("File Updated Successfully", safe=False)
        return JsonResponse("Failed to Update File")

    def delete(self, request, pk=None):
        file_to_delete = File.objects.get(fileId=pk)
        file_to_delete.delete()
        return JsonResponse("File Deleted Successfully", safe=False)