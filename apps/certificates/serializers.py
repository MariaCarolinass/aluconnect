from rest_framework import serializers
from apps.certificates.models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(many=False, read_only=True)
    course = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Certificate
        fields = [
            'id',
            'student',
            'course',
            'code',
            'text',
            'issued_at'
        ]
        read_only_fields = ['issued_at']
    
