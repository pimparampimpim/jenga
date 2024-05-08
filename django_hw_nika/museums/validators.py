from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re
from datetime import date, datetime

def street_name_validator(name: str) -> None:
    rule = re.compile(r'^[а-яА-ЯёЁa-zA-Z0-9 ]+$')
    if not rule.search(name):
        raise ValidationError(
            _('Street name contains incorrect symbols.'),
            params={'street_name': name}
        )


def house_number_validator(number: str) -> None:
    rule = re.compile(r'^[1-9]\d*(?: ?(?:([а-я]|[a-z])|[\/-] ?[1-9]+\d*([а-я]|[a-z])?))?$')
    if not rule.search(number):
        raise ValidationError(
            _("""Incorrect house number format. Use one of this:
12, 12а, 12А,12 А, 12 а, 12 б, 12 я, 121 б, 56/58, 56/58а, 56-58, 56 - 58, 56-58а"""),
            params={'house_number': number}
        )
    
def check_birthday(birthday: int) -> None:
    if birthday > date(date.today().year-6, date.today().month, date.today().day):
        raise ValidationError(
            _('You so young to work in museum!'),
            params={'birthday': birthday},
        )
    

def check_positive(floor) -> None:
    if floor < 0:
        raise ValidationError('value should be equal or greater than zero')  