import json

from django.contrib.gis.geos import Point, GEOSGeometry
from django.urls import reverse
import pytest

from apps.partner import factories, views, models


class TestViews:
    def setup(self):
        self.point = Point(15.0, 10.0, srid=4326)
        self.coverageArea = GEOSGeometry(json.dumps({
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [30.0, 20.0],
                        [45.0, 40.0],
                        [10.0, 40.0],
                        [30.0, 20.0]
                    ]
                ],
                [
                    [
                        [15.0, 5.0],
                        [40.0, 10.0],
                        [10.0, 20.0],
                        [5.0, 10.0],
                        [15.0, 5.0]
                    ]
                ]
            ]
        }))
        self.another_coverageArea = GEOSGeometry(json.dumps({
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [-30.0, -20.0],
                        [-45.0, -40.0],
                        [-10.0, -40.0],
                        [-30.0, -20.0]
                    ]
                ],
                [
                    [
                        [-15.0, -5.0],
                        [-40.0, -10.0],
                        [-10.0, -20.0],
                        [-5.0, -10.0],
                        [-15.0, -5.0]
                    ]
                ]
            ]
        }))
        self.view = views.PartnerViewSet()
        self.view.kwargs = {'coordinates': f'{self.point.x},{self.point.y}'}

    @pytest.mark.unittest
    def test_get_point_from_lookup(self):
        expected = self.point
        point = self.view.get_point_from_lookup()
        assert point == expected

    @pytest.mark.integration
    @pytest.mark.django_db
    def test_get_nearest(self, client):
        instance = factories.PartnerFactory.create(
            address=self.point,
            coverageArea=self.coverageArea
        )
        url = reverse('partner-nearest-detail', kwargs=self.view.kwargs)
        response = client.get(url)
        data = response.json()
        assert data.get('id') == instance.pk

    @pytest.mark.integration
    @pytest.mark.django_db
    def test_get_partner(self, client):
        instance = factories.PartnerFactory.create(
            address=self.point,
            coverageArea=self.coverageArea
        )
        url = reverse('partner-detail', kwargs={'pk': instance.pk})
        response = client.get(url)
        data = response.json()
        assert data.get('id') == instance.pk

    @pytest.mark.integration
    @pytest.mark.django_db
    def test_list_partners(self, client):
        expected = 5
        factories.PartnerFactory.create_batch(
            expected,
            address=self.point,
            coverageArea=self.coverageArea
        )
        url = reverse('partner-list')
        response = client.get(url)
        data = response.json()
        assert len(data) == expected

    @pytest.mark.integration
    @pytest.mark.django_db
    def test_list_nearest_partners(self, client):
        expected = 5
        factories.PartnerFactory.create_batch(
            expected,
            address=self.point,
            coverageArea=self.coverageArea
        )
        factories.PartnerFactory.create_batch(
            expected,
            address=self.point,
            coverageArea=self.another_coverageArea
        )
        url = reverse('partner-list')
        url = url + '?address={ "type": "Point", "coordinates": [15, 10] }'
        response = client.get(url)
        data = response.json()
        assert len(data) == expected
