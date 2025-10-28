from django.urls import path
from apps.certificates.views import CertificateListView

urlpatterns = [
    path('certificates', CertificateListView.as_view(), name='certificate-list'),
]
