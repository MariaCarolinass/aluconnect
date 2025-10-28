from django.contrib import admin
from apps.lessons.models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at', 'updated_at')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    ordering = ('course', 'order')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('course', 'title', 'content', 'order', 'duration', 'video_url')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
        }),
    )