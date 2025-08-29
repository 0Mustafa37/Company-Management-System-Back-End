from rest_framework import serializers

from company.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class ReadCompanySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    num_of_employee = serializers.IntegerField()
    num_of_department = serializers.IntegerField()
    num_of_project = serializers.IntegerField()
