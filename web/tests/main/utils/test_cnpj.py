from django.core.exceptions import ValidationError
import pytest

from main.utils import cnpj


class TestCnpj:
    def setup(self):
        self.exceptional_cases_list = [
            "11111111111111",
            "22222222222222",
            "33333333333333",
            "44444444444444",
            "55555555555555",
            "66666666666666",
            "77777777777777",
            "88888888888888",
            "99999999999999",
            "00000000000000"
        ]
        self.valid_cnpj_list = [
            '06.990.590/0001-23',
            '22.346.483/0001-13',
            '07.526.557/0001-00',
            '13.638.767/0001-92',
            '23.412.247/0001-10',
            '06990590000123',
            '22346483000113',
            '07526557000100',
            '13638767000192',
            '23412247000110'
        ]
        self.cnpj_list_with_wrong_verification_digits = [
            '06.990.590/0001-12',
            '22.346.483/0001-34',
            '07.526.557/0001-56',
            '13.638.767/0001-78',
            '23.412.247/0001-90',
            '06990590000112',
            '22346483000134',
            '07526557000156',
            '13638767000178',
            '23412247000190'
        ]

    @pytest.mark.unittest
    @pytest.mark.parametrize('_', [_ for _ in range(20)])
    def test_generate_cnpj(self, _):
        document = cnpj.generate_cnpj()
        assert cnpj.validate_cnpj(document) is None

    @pytest.mark.unittest
    def test_generate_cnpj_first_digit(self):
        document = cnpj.remove_non_numeric(cnpj.generate_cnpj())
        first_digit = cnpj.generate_cnpj_first_digit(document)

        expected = document[-2]
        assert first_digit == expected

    @pytest.mark.unittest
    def test_generate_cnpj_first_digit_for_exceptional_cases(self):
        expected = '0'

        for document in self.exceptional_cases_list:
            first_digit = cnpj.generate_cnpj_first_digit(document)
            assert first_digit == expected

    @pytest.mark.unittest
    def test_generate_cnpj_second_digit(self):
        document = cnpj.remove_non_numeric(cnpj.generate_cnpj())
        second_digit = cnpj.generate_cnpj_second_digit(document)

        expected = document[-1]
        assert second_digit == expected

    @pytest.mark.unittest
    def test_generate_cnpj_second_digit_for_exceptional_cases(self):
        expected = '0'

        for document in self.exceptional_cases_list:
            second_digit = cnpj.generate_cnpj_second_digit(document)
            assert second_digit == expected

    @pytest.mark.unittest
    def test_remove_non_numeric(self):
        document = '123.456/78-9'
        expected = '123456789'

        assert cnpj.remove_non_numeric(document) == expected

    @pytest.mark.unittest
    def test_formatted_cnpj(self):
        expected = cnpj.generate_cnpj()
        document_without_special_chars = cnpj.remove_non_numeric(expected)

        assert cnpj.formatted_cnpj(document_without_special_chars) == expected

    @pytest.mark.unittest
    @pytest.mark.parametrize('document, expected', [
        ('6.990.590/0001-12', '06.990.590/0001-12',),
        ('7.526.557/0001-56', '07.526.557/0001-56',),
        ('6990590000112', '06.990.590/0001-12',),
        ('7526557000156', '07.526.557/0001-56')
    ])
    def test_formatted_cnpj_with_zeros_on_left(self, document, expected):
        document = cnpj.remove_non_numeric(document)
        assert cnpj.formatted_cnpj(document) == expected

    @pytest.mark.unittest
    def test_validate_cnpj_length_must_pass_only_numbers(self):
        expected_length = 14
        document = '1' * expected_length

        assert cnpj.validate_cnpj_length(document) is None

    @pytest.mark.unittest
    def test_validate_cnpj_length_must_pass_numbers_and_special_chars(self):
        expected_length = 14
        document = '1.' * expected_length

        assert cnpj.validate_cnpj_length(document) is None

    @pytest.mark.unittest
    def test_validate_cnpj_length_must_fail(self):
        expected_length = 14
        document = '1' * (expected_length + 1)

        with pytest.raises(ValidationError):
            cnpj.validate_cnpj_length(document)

    @pytest.mark.unittest
    def test_validate_cnpj_fails_for_exceptional_cases(self):
        expected_errors = len(self.exceptional_cases_list)
        errors_count = 0
        for document in self.exceptional_cases_list:
            try:
                cnpj.validate_cnpj(document)
            except ValidationError:
                errors_count += 1
                continue
            print(document)

        assert errors_count == expected_errors

    @pytest.mark.unittest
    def test_validate_cnpj_fails_for_wrong_verification_digits(self):
        expected_errors = len(self.cnpj_list_with_wrong_verification_digits)
        errors_count = 0
        for document in self.cnpj_list_with_wrong_verification_digits:
            try:
                cnpj.validate_cnpj(document)
            except ValidationError:
                errors_count += 1
                continue
            print(document)

        assert errors_count == expected_errors

    @pytest.mark.unittest
    def test_validate_cnpj_passes(self):
        for document in self.valid_cnpj_list:
            assert cnpj.validate_cnpj(document) is None
