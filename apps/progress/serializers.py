from rest_framework import serializers
from apps.progress.models import Progress


class ProgressSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Progress
        fields = [
            'id',
            'student',
            'student_name',
            'course',
            'course_title',
            'lesson',
            'lesson_title',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
