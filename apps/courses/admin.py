from django.contrib import admin
from apps.courses.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'get_instructors', 'created_at', 'updated_at')
    list_filter = ('instructors',)
    search_fields = ('title', 'instructors__username', 'instructors__email')
    ordering = ('title',)
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('instructors', 'students')

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'instructors', 'students')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def get_instructors(self, obj):
        return ", ".join([str(instrutor) for instrutor in obj.instructors.all()])
    get_instructors.short_description = 'Instrutores'
