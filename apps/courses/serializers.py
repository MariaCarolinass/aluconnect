from rest_framework import serializers
from apps.courses.models import Course
from apps.users.models import User


class CourseSerializer(serializers.ModelSerializer):
    instructors = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='INSTRUCTOR'),
        many=True,
        required=False
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructors', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_instructors(self, value):
        for user in value:
            if user.role != 'INSTRUCTOR':
                raise serializers.ValidationError(f"{user.get_full_name()} não é um instrutor.")
        return value


class CourseDetailSerializer(serializers.ModelSerializer):
    instructors = serializers.StringRelatedField(many=True)
    students = serializers.StringRelatedField(many=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructors', 'students', 'created_at', 'updated_at']
