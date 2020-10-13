from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from . import models, serializers, filters


class PartnerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = models.Partner.objects.all()
    serializer_class = serializers.PartnerSerializer
    filterset_class = filters.InsideCoverageAreaFilter
    filter_backends = (
        DjangoFilterBackend, filters.NearestAddressOrderingFilter
    )
    distance_ordering_filter_field = 'address'
