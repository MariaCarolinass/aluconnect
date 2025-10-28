from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.users.serializers import RegisterSerializer
from apps.users.models import User
from apps.users.serializers import LogoutSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.serializers import EmptySerializer

class RegisterView(generics.CreateAPIView):
    """
    Registra um novo usuário na plataforma.
    Acesso público.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LogoutView(APIView):
    """
    Realiza logout do usuário autenticado, invalidando o token de refresh.
    Requer autenticação.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = EmptySerializer

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data.get("refresh")
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Token inválido ou já expirado."}, status=status.HTTP_400_BAD_REQUEST)