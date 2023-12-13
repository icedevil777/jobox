from rest_framework import serializers

from industrial.models import Applicant


class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicant
        fields = '__all__'
        read_only_fields = ['user_email']
