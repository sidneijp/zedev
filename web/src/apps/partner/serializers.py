from rest_framework import serializers

from . import models


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Partner
        fields = '__all__'
