from django.contrib.gis.db import models


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
        return ''
