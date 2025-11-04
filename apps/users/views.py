from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.users.serializers import RegisterSerializer
from apps.users.constants import UserRole
from apps.users.serializers import LoginSerializer, LogoutSerializer, TokenSerializer, EmptySerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from django.core.exceptions import PermissionDenied


@extend_schema(
    summary="Criação de usuário por administrador",
    description="Permite que um administrador crie novos usuários com diferentes papéis.",
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(description="Usuário criado com sucesso."),
        403: OpenApiResponse(description="Acesso negado para usuários não administradores."),
    },
    tags=["admin users"],
    examples=[
        OpenApiExample(
            "Exemplo de Criação de Usuário",
            value={
                "email": "admin@example.com",
                "username": "admin_user",
                "password": "admin_password",
                "role": "ADMIN"
            },
            request_only=True
        )
    ]
)
class UserAdminCreateView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != UserRole.ADMIN:
            raise PermissionDenied("Apenas administradores podem criar usuários.")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {"success": True, "message": f"Usuário '{user.role}' criado com sucesso!", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
    
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({"success": False, "error": str(exc), "detail": "Você não tem permissão para realizar essa ação."}, status=status.HTTP_403_FORBIDDEN)
        return super().handle_exception(exc)


@extend_schema(
    summary="Login de usuário",
    description="Autentica o usuário e retorna os tokens de acesso e atualização (JWT).",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(response=TokenSerializer, description="Login realizado com sucesso."),
        400: OpenApiResponse(description="Credenciais inválidas.")
    },
    tags=["authentication"],
    examples=[
        OpenApiExample(
            "Exemplo de Login",
            value={"email": "student@example.com", "password": "senha_segura"},
            request_only=True
        )
    ]
)
class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        response_data = {
            "message": f"Login realizado com sucesso como {user.role}.",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "role": user.role
            },
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)


@extend_schema(
    summary="Registro de novo usuário",
    description="Cria um novo usuário na plataforma.",
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(description="Usuário criado com sucesso."),
        400: OpenApiResponse(description="Erro de validação."),
    },
    tags=["authentication"],
    examples=[
        OpenApiExample(
            "Exemplo de Registro",
            value={
                "email": "student@example.com",
                "username": "student123",
                "password": "senha_segura",
                "role": "STUDENT"
            },
            request_only=True
        )
    ]
)
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        response_data = {
            "message": "Usuário registrado com sucesso.",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "role": user.role
            },
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


@extend_schema(
    summary="Atualizar tokens JWT",
    description="Recebe um par de tokens (access e refresh) e retorna novos tokens válidos.",
    request=TokenSerializer,
    responses={
        200: OpenApiResponse(response=TokenSerializer, description="Tokens atualizados com sucesso."),
        400: OpenApiResponse(description="Token inválido ou expirado."),
    },
    tags=["authentication"],
    examples=[
        OpenApiExample(
            "Exemplo de Refresh",
            value={
                "access": "string",
                "refresh": "string"
            },
            request_only=True
        )
    ]
)
class CustomTokenRefreshView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data.get("refresh")
        try:
            refresh = RefreshToken(refresh_token)
            new_access = refresh.access_token
            return Response({
                "access": str(new_access),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Token inválido ou expirado."}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Logout de usuário",
    description="Realiza logout e invalida o token de atualização (refresh token).",
    request=LogoutSerializer,
    responses={
        200: OpenApiResponse(description="Logout realizado com sucesso."),
        400: OpenApiResponse(description="Token inválido ou já expirado."),
    },
    tags=["authentication"],
    examples=[
        OpenApiExample(
            "Exemplo de Logout",
            value={"refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."},
            request_only=True
        )
    ]
)
class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data.get("refresh")
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout realizado com sucesso."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Token inválido ou já expirado."}, status=status.HTTP_400_BAD_REQUEST)
        

@extend_schema(
    summary="Informações sobre Autenticação Social",
    description=(
        "Rotas de autenticação social são fornecidas por `social_django`.\n\n"
        "Exemplo:\n"
        "- `/auth/social/login/google-oauth2/`\n"
        "Essa rota seguem o fluxo OAuth2 padrão."
    ),
    tags=["authentication"]
)
class SocialAuthInfoView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmptySerializer

    def get(self, request):
        return Response({
            "message": "Rotas de autenticação social disponíveis em /auth/social/"
        })


@extend_schema(
    summary="Callback de autenticação social (JWT)",
    description=(
        "Endpoint chamado após a autenticação bem-sucedida via login social "
        "(ex: Google). Recebe tokens JWT gerados pelo backend e retorna "
        "os valores `access` e `refresh` para uso no frontend."
    ),
    tags=["authentication"],
    responses={
        200: OpenApiResponse(
            description="Tokens JWT retornados com sucesso.",
            examples=[
                OpenApiExample(
                    "Exemplo de sucesso",
                    value={
                        "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    }
                )
            ]
        ),
        400: OpenApiResponse(
            description="Erro na autenticação social.",
            examples=[
                OpenApiExample(
                    "Exemplo de erro",
                    value={"detail": "Autenticação social falhou."}
                )
            ]
        ),
    },
)
class SocialJWTCallbackView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = EmptySerializer
    
    def get(self, request, *args, **kwargs):
        access = request.query_params.get("access")
        refresh = request.query_params.get("refresh")

        if not access or not refresh:
            return Response({"detail": "Autenticação social falhou."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "access": access,
            "refresh": refresh
        })
