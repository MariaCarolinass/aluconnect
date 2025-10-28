from django.contrib import admin
from apps.instructors.models import Instructor


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('user',)

    fieldsets = (
        (None, {
            'fields': ('user', 'bio')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
