from django.contrib.gis.db import models
from django.contrib.gis.db.models.functions import GeometryDistance

from main.utils import remove_non_numeric


class Partner(models.Model):
    tradingName = models.CharField(max_length=100)
    ownerName = models.CharField(max_length=50)
    document = models.CharField(max_length=14, unique=True)
    coverageArea = models.MultiPolygonField()
    address = models.PointField()

    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self):
        return f'{self.document}'

    def save(self, *args, **kwargs):
        self.clean_document()
        super().save(*args, **kwargs)

    def clean_document(self):
        if self.document:
            self.document = remove_non_numeric(self.document)

    @classmethod
    def get_nearest_inside_coverage(cls, point, queryset=None):
        queryset = queryset or cls.objects
        queryset = queryset.filter(
            coverageArea__contains=point
        ).order_by(
            GeometryDistance('address', point)
        )

        return queryset.first()
