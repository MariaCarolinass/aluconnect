from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from apps.certificates.models import Certificate
from apps.certificates.serializers import CertificateSerializer


class CertificateListView(generics.ListAPIView):
    """
    Lista todos os certificados emitidos para o usuário autenticado.
    """
    serializer_class = CertificateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Certificate.objects.filter(student=self.request.user)
