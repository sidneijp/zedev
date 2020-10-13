import factory.django

from main import utils

from . import models


class PartnerFactory(factory.django.DjangoModelFactory):
    document = factory.LazyAttribute(lambda x: utils.generate_cnpj())

    class Meta:
        model = models.Partner
