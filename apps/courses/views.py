from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from apps.users.serializers import EmptySerializer
from apps.courses.models import Course
from apps.courses.serializers import CourseSerializer, CourseDetailSerializer
from apps.users.constants import UserRole
from rest_framework.exceptions import PermissionDenied, ValidationError
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse


@extend_schema(
    summary="Criação de curso",
    description="Permite que **instrutores** ou **administradores** criem novos cursos. "
                "O instrutor logado será automaticamente vinculado ao curso criado.",
    request=CourseSerializer,
    responses={
        201: OpenApiResponse(description="Curso criado com sucesso."),
        400: OpenApiResponse(description="Curso já existente ou instrutor já vinculado."),
        403: OpenApiResponse(description="Acesso negado para usuários não autorizados."),
    },
    tags=["courses"],
    examples=[
        OpenApiExample(
            "Exemplo de Criação de Curso",
            value={
                "title": "Introdução à Programação",
                "description": "Curso básico sobre conceitos de programação."
            },
            request_only=True
        )
    ]
)
class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user

        if user.role not in [UserRole.INSTRUCTOR, UserRole.ADMIN]:
            raise PermissionDenied("Apenas instrutores ou administradores podem criar cursos.")

        title = serializer.validated_data.get("title")
        if Course.objects.filter(title__iexact=title).exists():
            raise ValidationError({"title": f"O curso '{title}' já existe."})

        course = serializer.save()

        if user.role == UserRole.INSTRUCTOR:
            if not course.instructors.filter(pk=user.pk).exists():
                course.instructors.add(user)

        return course

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = self.perform_create(serializer)
        return Response(
            {
                "success": True,
                "message": f"Curso '{course.title}' criado e vinculado ao instrutor com sucesso!",
                "data": self.get_serializer(course).data,
            },
            status=status.HTTP_201_CREATED,
        )

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"success": False, "error": str(exc), "detail": "Você não tem permissão para realizar essa ação."},
                status=status.HTTP_403_FORBIDDEN,
            )
        if isinstance(exc, ValidationError):
            return Response(
                {"success": False, "errors": exc.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().handle_exception(exc)


@extend_schema(
    summary="Listagem de cursos",
    description="Retorna uma lista de todos os cursos disponíveis na plataforma.",
    responses={200: CourseDetailSerializer(many=True)},
    tags=["courses"],
)
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [AllowAny]


@extend_schema(
    summary="Detalhes do curso",
    description="Retorna os detalhes de um curso específico com base no ID fornecido.",
    responses={200: CourseDetailSerializer()},
    tags=["courses"],
)
class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'


@extend_schema(
    summary="Atualização de curso",
    description="Permite que usuários autenticados atualizem os dados de um curso específico.",
    request=CourseSerializer,
    responses={200: OpenApiResponse(description="Curso atualizado com sucesso.")},
    tags=["courses"],
)
class CourseUpdateView(generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_object(self):
        course = super().get_object()
        user = self.request.user
        if user.role == UserRole.ADMIN or course.instructors.filter(id=user.id).exists():
            return course
        raise PermissionDenied("Apenas instrutores do curso ou administradores podem editar.")

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"success": False, "error": str(exc), "detail": "Você não tem permissão para realizar essa ação."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)


@extend_schema(
    summary="Inscrição em curso",
    description="Permite que o usuário autenticado se inscreva em um curso específico.",
    responses={200: OpenApiResponse(description="Inscrição realizada com sucesso.")},
    tags=["courses"],
)
class EnrollStudentView(generics.GenericAPIView):
    serializer_class = EmptySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        course = get_object_or_404(Course, id=id)

        if request.user.role != UserRole.STUDENT:
            raise PermissionDenied("Apenas estudantes podem se inscrever em cursos.")

        if course.students.filter(id=request.user.id).exists():
            return Response({"detail": "Você já está inscrito neste curso."}, status=status.HTTP_200_OK)

        course.students.add(request.user)
        return Response({"detail": "Inscrição realizada com sucesso."}, status=status.HTTP_200_OK)

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"success": False, "error": str(exc), "detail": "Você não tem permissão para realizar essa ação."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)


@extend_schema(
    summary="Cursos do aluno",
    description="Lista os cursos em que o aluno autenticado está matriculado.",
    responses={200: CourseDetailSerializer(many=True)},
    tags=["courses"],
)
class StudentCoursesView(generics.ListAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != UserRole.STUDENT:
            raise PermissionDenied("Apenas estudantes podem acessar seus cursos.")
        return Course.objects.filter(students=user)

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"success": False, "error": str(exc), "detail": "Você não tem permissão para realizar essa ação."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)


@extend_schema(
    summary="Cursos do instrutor",
    description="Lista os cursos ministrados pelo instrutor autenticado.",
    responses={200: CourseDetailSerializer(many=True)},
    tags=["courses"],
)
class InstructorCoursesView(generics.ListAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != UserRole.INSTRUCTOR:
            raise PermissionDenied("Apenas instrutores podem acessar seus cursos.")
        return Course.objects.filter(instructors=user)

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"success": False, "error": str(exc), "detail": "Você não tem permissão para realizar essa ação."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().handle_exception(exc)