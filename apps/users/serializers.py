from rest_framework import serializers, status
from django.contrib.auth import authenticate
from apps.users.models import User
from apps.users.constants import UserRole
from apps.students.models import Student
from apps.instructors.models import Instructor
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
        required=True,
    )

    def validate(self, data):
        user = authenticate(
            username=data.get("email"),
            password=data.get("password")
        )
        if not user:
            raise serializers.ValidationError("Credenciais inválidas.")

        if user.role == UserRole.INSTRUCTOR and not user.is_active:
            raise PermissionDenied("Instrutor inativo. Acesso negado.")

        if user.role == UserRole.STUDENT:
            student_profile = getattr(user, 'student_profile', None)
            if student_profile and student_profile.is_blocked():
                blocked_until = student_profile.blocked_until.strftime('%Y-%m-%d %H:%M:%S')
                raise PermissionDenied(f"Acesso temporariamente bloqueado até {blocked_until}.")

        data['user'] = user
        return data
    
    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({"success": False, "error": str(exc), "detail": "Você não tem permissão para realizar essa ação."}, status=status.HTTP_403_FORBIDDEN)
        return super().handle_exception(exc)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        required=True
    )
    role = serializers.ChoiceField(choices=UserRole.CHOICES, required=True)

    class Meta:
        model = User
        fields = ["email", "username", "password", "role"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value

    def create(self, validated_data):
        role = validated_data.pop("role", UserRole.STUDENT)
        user = User.objects.create_user(**validated_data, role=role)

        if role == UserRole.STUDENT:
            Student.objects.create(user=user)
        elif role == UserRole.INSTRUCTOR:
            Instructor.objects.create(user=user)
        elif role == UserRole.ADMIN:
            pass

        return user


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField(help_text="Token de acesso JWT.")
    refresh = serializers.CharField(help_text="Token de atualização JWT.")
    

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class EmptySerializer(serializers.Serializer):
    pass