from rest_framework import serializers
from apps.instructors.models import Instructor


class InstructorSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Instructor
        fields = [
            'id',
            'username',
            'email',
            'title',
            'bio',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
