from rest_framework import mixins, viewsets

from . import models, serializers


class PartnerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.Partner.objects.all()
    serializer_class = serializers.PartnerSerializer
