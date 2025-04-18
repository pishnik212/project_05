from django.shortcuts import render

# Create your views here.
from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import JsonResponse
from .models import University
from .serializers import UniversitySerializer


class UniversityView(APIView):

    def post(self, request):
        data = request.data
        serializer = UniversitySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Университет добавлен успешно",          safe=False)
        return JsonResponse("Failed to Add University", safe=False)


    def get_university(self, pk):
        try:
            university = University.objects.get(universityId=pk)
            return university
        except:
            return JsonResponse("University Does Not Exist", safe=False)

    def get(self, request, pk=None):
        if pk:
            data = self.get_university(pk)
            serializer = UniversitySerializer(data)
        else:
            data = University.objects.all()
            serializer = UniversitySerializer(data, many=True)
        return Response(serializer.data)


    def put(self, request, pk=None):
        university_to_update = University.objects.get(universityId=pk)
        serializer = UniversitySerializer(instance=university_to_update, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("University Updated Successfully", safe=False)
        return JsonResponse("Failed to Update University")

    def delete(self, request, pk=None):
        university_to_delete = University.objects.get(universityId=pk)
        university_to_delete.delete()
        return JsonResponse("University Deleted Successfully", safe=False)