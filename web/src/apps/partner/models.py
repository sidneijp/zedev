from django.db import models


class Partner(models.Model):
    class Meta:
        verbose_name = 'Partner'
        verbose_name_plural = 'Partners'

    def __str__(self):
        return ''
