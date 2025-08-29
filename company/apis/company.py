from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from company.models import Company
from company.serializers import CompanySerializer, ReadCompanySerializer


class CompanyAPIView(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ReadCompanySerializer
        return CompanySerializer

    def get_queryset(self):
        return self.queryset.annotate(
            num_of_employee=Count("company_employee", distinct=True),
            num_of_department=Count("departments", distinct=True),
            num_of_project=Count("company_projects", distinct=True),
        )
