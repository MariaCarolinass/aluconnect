from rest_framework import serializers
from apps.users.models import User
from apps.users.models import UserRole


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"},
        help_text="A senha deve conter pelo menos 8 caracteres."
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'role']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'role': {'default': UserRole.STUDENT}
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email já está em uso.")
        return value
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class EmptySerializer(serializers.Serializer):
    pass


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()