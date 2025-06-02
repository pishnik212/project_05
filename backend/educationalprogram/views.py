from django.shortcuts import render

from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import JsonResponse
from .models import Educationalprogram
from .serializers import EducationalprogramSerializer


class EducationalprogramView(APIView):

    def post(self, request):
        data = request.data
        serializer = EducationalprogramSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Образовательная программа добавлена успешно",          safe=False)
        return JsonResponse("Не удалось добавить образовательную программу", safe=False)


    def get_educationalprogram(self, pk):
        try:
            ep = Educationalprogram.objects.get(epId=pk)
            return ep
        except:
            return JsonResponse("University Does Not Exist", safe=False)

    def get(self, request, pk=None):
        if pk:
            data = self.get_educationalprogram(pk)
            serializer = EducationalprogramSerializer(data)
        else:
            data = Educationalprogram.objects.all()
            serializer = EducationalprogramSerializer(data, many=True)
        return Response(serializer.data)


    def put(self, request, pk=None):
        educationalprogram_to_update = Educationalprogram.objects.get(epId=pk)
        serializer = EducationalprogramSerializer(instance=educationalprogram_to_update, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Educationalprogram Updated Successfully", safe=False)
        return JsonResponse("Failed to Update Educationalprogram")

    def delete(self, request, pk=None):
        educationalprogram_to_delete = Educationalprogram.objects.get(epId=pk)
        educationalprogram_to_delete.delete()
        return JsonResponse("Educationalprogram Deleted Successfully", safe=False)
