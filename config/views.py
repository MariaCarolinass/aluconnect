from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny


class EmptySerializer(serializers.Serializer):
    pass


class IndexView(APIView):
    """
    Endpoint público de boas-vindas à API AluConnect.
    """
    serializer_class = EmptySerializer
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Welcome to AluConnect API"}, status=status.HTTP_200_OK)
