from django.contrib.gis.db.models.functions import GeometryDistance
from django.contrib.gis.geos import Point, GEOSGeometry
from rest_framework.exceptions import ParseError
from rest_framework_gis.filters import (
    DistanceToPointOrderingFilter, GeometryFilter
)
from rest_framework_gis.filterset import GeoFilterSet

from . import models


class GeometryDistanceToPointOrderingFilter(DistanceToPointOrderingFilter):
    ordering = None

    def filter_queryset(self, request, queryset, view):
        if not GeometryDistance:
            raise ValueError(
                'GeometryDistance not available on this version of django'
            )

        filter_field = getattr(view, 'distance_ordering_filter_field', None)
        if not filter_field:
            return queryset

        point = self.get_filter_point(request, srid=self.srid)
        if not point:
            return queryset

        order = self.get_ordering(request)
        if order == 'desc':
            return queryset.order_by(-GeometryDistance(filter_field, point))
        else:
            return queryset.order_by(GeometryDistance(filter_field, point))

    def get_filter_point(self, request, **kwargs):
        point_string = request.query_params.get(self.point_param, None)
        if not point_string:
            return None

        try:
            geom = GEOSGeometry(point_string)
            x, y = geom.coords
        except ValueError:
            raise ParseError(
                'Invalid geometry string supplied for parameter {0}'.format(
                    self.point_param
                )
            )

        p = Point(x, y, **kwargs)
        return p

    def get_ordering(self, request):
        return request.query_params.get(self.order_param) or self.ordering


class NearestAddressOrderingFilter(GeometryDistanceToPointOrderingFilter):
    point_param = 'address'
    ordering = 'asc'


class InsideCoverageAreaFilter(GeoFilterSet):
    address = GeometryFilter(field_name='coverageArea', lookup_expr='contains')

    class Meta:
        model = models.Partner
        fields = ('address',)
