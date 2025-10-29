from rest_framework import serializers
from apps.courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    instructors = serializers.StringRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructors', 'created_at', 'updated_at']
        read_only_fields = ['instructors', 'created_at', 'updated_at']

    def validate_title(self, value):
        if Course.objects.filter(title__iexact=value).exists():
            raise serializers.ValidationError(f"O curso '{value}' já existe.")
        return value

    def validate_instructors(self, value):
        for instructor in value:
            if not instructor.is_active:
                raise serializers.ValidationError(f"{instructor.user.username} está inativo.")
        return value


class CourseDetailSerializer(serializers.ModelSerializer):
    instructors = serializers.StringRelatedField(many=True)
    students = serializers.StringRelatedField(many=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructors', 'students', 'created_at', 'updated_at']
