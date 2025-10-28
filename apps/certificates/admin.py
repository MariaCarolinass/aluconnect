from django.contrib import admin
from apps.certificates.models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('code', 'student', 'course', 'issued_at')
    list_filter = ('course', 'issued_at')
    search_fields = ('code', 'student__username', 'student__email', 'course__title')
    ordering = ('-issued_at',)
    readonly_fields = ('issued_at',)

    fieldsets = (
        ('Informações do certificado', {
            'fields': ('code', 'student', 'course')
        }),
        ('Data de emissão', {
            'fields': ('issued_at',)
        }),
    )
