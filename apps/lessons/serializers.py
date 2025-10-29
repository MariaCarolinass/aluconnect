from rest_framework import serializers
from apps.lessons.models import Lesson
from apps.courses.models import Course


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField(many=False, read_only=True)

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

    def validate(self, attrs):
        """
        Valida se a ordem da aula é única dentro do curso.
        """
        course = attrs.get('course') or self.context.get('course')
        order = attrs.get('order')

        if course and order:
            if Lesson.objects.filter(course=course, order=order).exists():
                raise serializers.ValidationError({
                    'order': 'Já existe uma aula com essa ordem neste curso.'
                })
        return attrs

    def create(self, validated_data):
        """
        Define o próximo número de ordem se não for informado.
        """
        course = validated_data.get('course') or self.context.get('course')

        if not course:
            raise serializers.ValidationError({'course': 'Curso é obrigatório.'})

        if 'order' not in validated_data or validated_data['order'] is None:
            last_order = (
                Lesson.objects.filter(course=course)
                .aggregate(max_order=serializers.Max('order'))
                .get('max_order')
            )
            validated_data['order'] = (last_order or 0) + 1

        return Lesson.objects.create(**validated_data)