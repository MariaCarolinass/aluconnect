from rest_framework import serializers
from apps.lessons.models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'course',
            'title',
            'content',
            'order',
            'duration',
            'video_url',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_order(self, value):
        course = self.initial_data.get('course')
        if course and Lesson.objects.filter(course_id=course, order=value).exists():
            raise serializers.ValidationError("Já existe uma aula com essa ordem neste curso.")
        return value
