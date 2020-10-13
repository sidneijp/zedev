from django.contrib.gis.geos import GEOSGeometry
import pytest
import json

from apps.partner import models, factories


class TestPartner:
    def setup(self):
        self.model = models.Partner
        self.model_factory = factories.PartnerFactory
        self.instance = factories.PartnerFactory.build()
        self.furthest_address = GEOSGeometry(json.dumps({
            "type": "Point", "coordinates": [-47.57421, -21.785741]
        }))
        self.nearest_address = GEOSGeometry(json.dumps({
            "type": "Point", "coordinates": [20, 10]
        }))
        self.point_inside_coverage = GEOSGeometry(json.dumps(
            {"type": "Point", "coordinates": [15, 10]}
        ))
        self.point_outside_coverage = GEOSGeometry(json.dumps(
            {"type": "Point", "coordinates": [0, 0]}
        ))
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

    @pytest.mark.unittest
    def test_str(self):
        assert str(self.instance) == f'{self.instance.document}'

    @pytest.mark.unittest
    @pytest.mark.django_db
    def test_get_nearest_inside_coverage_without_coverage(self):
        factories.PartnerFactory.create(
            coverageArea=self.coverageArea,
            address=self.furthest_address
        )
        factories.PartnerFactory.create(
            coverageArea=self.coverageArea,
            address=self.nearest_address
        )

        nearest = models.Partner.get_nearest_inside_coverage(
            self.point_outside_coverage
        )

        assert nearest is None

    @pytest.mark.unittest
    @pytest.mark.django_db
    def test_get_nearest_inside_coverage_with_coverage(self):
        factories.PartnerFactory.create(
            coverageArea=self.coverageArea,
            address=self.furthest_address
        )
        expected = factories.PartnerFactory.create(
            coverageArea=self.coverageArea,
            address=self.nearest_address
        )

        nearest = models.Partner.get_nearest_inside_coverage(
            self.point_inside_coverage
        )

        assert nearest == expected
