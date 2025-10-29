from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers import EmptySerializer


class IndexView(APIView):
    """
    Endpoint público de boas-vindas à API AluConnect.
    """
    serializer_class = EmptySerializer

    def get(self, request):
        return Response({"message": "Welcome to AluConnect API"}, status=status.HTTP_200_OK)
