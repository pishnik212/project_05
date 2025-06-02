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
            return JsonResponse("Учетная запись сотрудника создана успешно", safe=False)
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
            return JsonResponse("Учетная запись сотрудника обновлена успешно", safe=False)
        return JsonResponse(serializer.errors, safe=False)

    def delete(self, request, pk=None):
        officer = self.get_officer(pk)
        officer.user.delete()
        officer.delete()
        return JsonResponse("Officer and User deleted successfully", safe=False)


@api_view(['GET'])
def get_officer_by_user_id(request, user_id):
    try:
        # Лог
        print(f"Looking for officer with user_id: {user_id}")

        # офицер по user_id
        officer = Officer.objects.get(user__id=user_id)

        # Лог данные офицера
        print(f"Found officer: {officer.FirstName} {officer.LastName}")

        serializer = OfficerSerializer(officer)
        return Response(serializer.data)

    except Officer.DoesNotExist:
        print(f"Учетная запись сотрудника с user_id {user_id} не найдена")
        return Response({"error": "Учетная запись сотрудника не найдена"}, status=404)
    except Exception as e:
        # Лог ошибки
        print(f"Error: {str(e)}")
        return Response({"error": str(e)}, status=500)






