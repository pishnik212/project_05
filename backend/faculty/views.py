from django.shortcuts import render

from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import JsonResponse
from .models import Faculty
from .serializers import FacultySerializer


class FacultyView(APIView):

    def post(self, request):
        data = request.data
        serializer = FacultySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Faculty Added Successfully",          safe=False)
        return JsonResponse("Failed to Add Faculty", safe=False)


    def get_faculty(self, pk):
        try:
            ep = Faculty.objects.get(facultyId=pk)
            return ep
        except:
            return JsonResponse("University Does Not Exist", safe=False)

    def get(self, request, pk=None):
        if pk:
            data = self.get_faculty(pk)
            serializer = FacultySerializer(data)
        else:
            data = Faculty.objects.all()
            serializer = FacultySerializer(data, many=True)
        return Response(serializer.data)


    def put(self, request, pk=None):
        faculty_to_update = Faculty.objects.get(facultyId=pk)
        serializer = FacultySerializer(instance=faculty_to_update, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Faculty Updated Successfully", safe=False)
        return JsonResponse("Failed to Update Faculty")

    def delete(self, request, pk=None):
        faculty_to_delete = Faculty.objects.get(facultyId=pk)
        faculty_to_delete.delete()
        return JsonResponse("Faculty Deleted Successfully", safe=False)
