from django.http.response import JsonResponse, Http404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Officer
from .serializers import OfficerSerializer
from django.core.exceptions import ObjectDoesNotExist

class OfficerView(APIView):

    def post(self, request):
        serializer = OfficerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Officer and User created successfully", safe=False)
        return JsonResponse(serializer.errors, safe=False)

    def get_officer(self, pk):
        try:
            return Officer.objects.get(officerId=pk)
        except Officer.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            officer = self.get_officer(pk)
            serializer = OfficerSerializer(officer)
        else:
            officers = Officer.objects.all()
            serializer = OfficerSerializer(officers, many=True)
        return Response(serializer.data)

    def put(self, request, pk=None):
        officer = self.get_officer(pk)
        serializer = OfficerSerializer(instance=officer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse("Officer updated successfully", safe=False)
        return JsonResponse(serializer.errors, safe=False)

    def delete(self, request, pk=None):
        officer = self.get_officer(pk)
        officer.user.delete()  # Удаляем также и пользователя
        officer.delete()
        return JsonResponse("Officer and User deleted successfully", safe=False)


@api_view(['GET'])
def get_officer_by_user_id(request, user_id):
    try:
        # Логируем user_id, чтобы убедиться, что он передается правильно
        print(f"Looking for officer with user_id: {user_id}")

        # Получаем офицера по user_id
        officer = Officer.objects.get(user__id=user_id)

        # Логируем данные офицера, чтобы убедиться, что мы его нашли
        print(f"Found officer: {officer.FirstName} {officer.LastName}")

        serializer = OfficerSerializer(officer)
        return Response(serializer.data)

    except Officer.DoesNotExist:
        print(f"Officer with user_id {user_id} not found.")
        return Response({"error": "Officer not found"}, status=404)
    except Exception as e:
        # Логируем ошибку
        print(f"Error: {str(e)}")
        return Response({"error": str(e)}, status=500)






