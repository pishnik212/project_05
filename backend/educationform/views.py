from django.shortcuts import render

# Create your views here.
from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import JsonResponse
from .models import Educationform
from .serializers import EducationformSerializer


class EducationformView(APIView):

    def post(self, request):
        data = request.data
        serializer = EducationformSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Educationform Added Successfully",          safe=False)
        return JsonResponse("Failed to Add Educationform", safe=False)


    def get_educationform(self, pk):
        try:
            ep = Educationform.objects.get(efId=pk)
            return ep
        except:
            return JsonResponse("University Does Not Exist", safe=False)

    def get(self, request, pk=None):
        if pk:
            data = self.get_educationform(pk)
            serializer = EducationformSerializer(data)
        else:
            data = Educationform.objects.all()
            serializer = EducationformSerializer(data, many=True)
        return Response(serializer.data)


    def put(self, request, pk=None):
        educationform_to_update = Educationform.objects.get(efId=pk)
        serializer = EducationformSerializer(instance=educationform_to_update, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Educationform Updated Successfully", safe=False)
        return JsonResponse("Failed to Update Educationform")

    def delete(self, request, pk=None):
        educationform_to_delete = Educationform.objects.get(efId=pk)
        educationform_to_delete.delete()
        return JsonResponse("Educationform Deleted Successfully", safe=False)