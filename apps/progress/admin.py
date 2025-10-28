from django.contrib import admin
from apps.progress.models import Progress


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'lesson', 'status', 'updated_at')
    list_filter = ('status', 'course')
    search_fields = ('student__username', 'student__email', 'lesson__title', 'course__title')
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Informações de progresso', {
            'fields': ('student', 'course', 'lesson', 'status')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at')
        }),
    )
