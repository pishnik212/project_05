from django.http.response import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http.response import JsonResponse
from .models import City
from .serializers import CitySerializer


class CityView(APIView):


    def get_city(self, pk):
        try:
            city = City.objects.get(cityId=pk)
            return city
        except:
            return JsonResponse("City Does Not Exist", safe=False)

    def get(self, request, pk=None):
        if pk:
            data = self.get_city(pk)
            serializer = CitySerializer(data)
        else:
            data = City.objects.all()
            serializer = CitySerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = CitySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Город успешно добавлен", safe=False)
        return JsonResponse("Не удалось выполнить добавление города", safe=False)

    def put(self, request, pk=None):
        city_to_update = City.objects.get(cityId=pk)
        serializer = CitySerializer(instance=city_to_update, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("City Updated Successfully", safe=False)
        return JsonResponse("Failed to Update City")

    def delete(self, request, pk=None):
        city_to_delete = City.objects.get(cityId=pk)
        city_to_delete.delete()
        return JsonResponse("City Deleted Successfully", safe=False)




