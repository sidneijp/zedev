import factory.django

from . import models


class PartnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Partner
