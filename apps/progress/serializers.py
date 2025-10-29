from rest_framework import serializers
from apps.progress.models import Progress


class ProgressSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(many=False, read_only=True)
    lesson = serializers.StringRelatedField(many=False, read_only=True)
    course = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Progress
        fields = [
            'id',
            'student',
            'course',
            'lesson',
            'status',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
