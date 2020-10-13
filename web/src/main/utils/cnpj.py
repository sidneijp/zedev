import random
import re
from django.core.exceptions import ValidationError


def validate_cnpj_special_cases(cnpj: str) -> None:
    cleaned_cnpj = remove_non_numeric(cnpj)
    all_digits_are_equal = len(set(cleaned_cnpj)) == 1
    if all_digits_are_equal:
        message = "Invalid document"
        raise ValidationError(message)


def validate_cnpj_length(cnpj: str) -> None:
    cleaned_cnpj = remove_non_numeric(cnpj)
    if len(cleaned_cnpj) != 14:
        message = "Document must has 14 digits"
        raise ValidationError(message)


def validate_cnpj(cnpj: str) -> None:
    validate_cnpj_length(cnpj)
    validate_cnpj_special_cases(cnpj)
    cnpj = remove_non_numeric(cnpj)

    if cnpj[-2] != generate_cnpj_first_digit(cnpj) \
            or cnpj[-1] != generate_cnpj_second_digit(cnpj):
        message = "Invalid document"
        raise ValidationError(message)


def generate_cnpj_first_digit(cnpj: str) -> str:
    exceptional_cases_list = [
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
    if cnpj in exceptional_cases_list:
        return '0'

    total = 0
    weights = list(range(5, 1, -1)) + list(range(9, 1, -1))
    for i in range(12):
        total += int(cnpj[i]) * weights[i]

    modulo = total % 11
    digit = 0 if modulo < 2 else 11 - modulo

    return str(digit)


def generate_cnpj_second_digit(cnpj: str) -> str:
    exceptional_cases_list = [
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
    if cnpj in exceptional_cases_list:
        return '0'

    total = 0
    weights = list(range(6, 1, -1)) + list(range(9, 1, -1))
    for i in range(13):
        total += int(cnpj[i]) * weights[i]

    modulo = total % 11
    digit = 0 if modulo < 2 else 11 - modulo

    return str(digit)


def generate_cnpj():
    def calculate_special_digit(reversed_cnpj):
        special_digit = 0
        for index, digit in enumerate(reversed_cnpj):
            special_digit += digit * (index % 8 + 2)

        special_digit = 11 - special_digit % 11
        return special_digit if special_digit < 10 else 0

    reversed_cnpj = [1, 0, 0, 0] + [random.randint(0, 9) for _ in range(8)]
    for _ in range(2):
        verification_digit = [calculate_special_digit(reversed_cnpj)]
        reversed_cnpj = verification_digit + reversed_cnpj

    cnpj = str(reversed_cnpj[::-1])
    return formatted_cnpj(cnpj)


def formatted_cnpj(cnpj: str) -> str:
    cnpj = remove_non_numeric(cnpj)
    if len(cnpj) < 14:
        cnpj = cnpj.zfill(14)
    return '{}.{}.{}/{}-{}'.format(
        cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:]
    )


def remove_non_numeric(numeric_string: str) -> str:
    cleaned_string = re.sub("[^0-9]", "", numeric_string)
    return cleaned_string
