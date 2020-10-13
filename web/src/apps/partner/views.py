from django.contrib.gis.geos import Point
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from rest_framework import mixins, viewsets
from rest_framework.response import Response

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

    def nearest(self, request, *args, **kwargs):
        instance = self.get_nearest_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_nearest_object(self):
        point = self.get_point_from_lookup()
        queryset = self.filter_queryset(self.get_queryset())

        obj = models.Partner.get_nearest_inside_coverage(
            point, queryset=queryset
        )
        if obj is None:
            raise Http404

        self.check_object_permissions(self.request, obj)
        return obj

    def get_point_from_lookup(self):
        coordinates = self.kwargs['coordinates'].split(',')
        try:
            x, y = [float(coord.strip()) for coord in coordinates]
        except (TypeError, ValueError):
            raise Http404
        return Point(x, y, srid=4326)
