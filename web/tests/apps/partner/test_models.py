import pytest

from apps.partner import models, factories


class TestPartner:
    def setup(self):
        self.model = models.Partner
        self.model_factory = factories.PartnerFactory
        self.instance = factories.PartnerFactory.build()

    @pytest.mark.unittest
    @pytest.mark.skip
    @pytest.mark.parametrize('expected', [
        [''],
    ])
    def test_str(self, expected):
        assert str(self.instance) == expected
