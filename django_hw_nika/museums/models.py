from django.db import models
from uuid import uuid4
from datetime import datetime, date, timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .validators import street_name_validator, house_number_validator, check_birthday, check_positive

def get_datetime():
    return datetime.now(timezone.utc)

class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True #чтобы не создавались экземпляры моделей

def check_created(dt: datetime):
    if dt > get_datetime():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'created': dt},
        )

def check_modified(dt: datetime):
    if dt > get_datetime():
        raise ValidationError(
            _('Date and time is bigger than current!'),
            params={'modified': dt},
        )

class CreatedMixin(models.Model):
    created = models.DateTimeField(
        _('created'),
        null=True, blank=True,
        default=get_datetime,
        validators=[check_created],
    )

    class Meta:
        abstract = True

class ModifiedMixin(models.Model):
    modified = models.DateTimeField(
        _('modified'),
        null=True, blank=True,
        default=get_datetime,
        validators=[check_modified]
    )

    class Meta:
        abstract = True

MAX_LENGTH_TITLE = 255
MAX_LENGTH_ADRESS = 300
MAX_LENGTH_NAME = 80
MAX_LENGTH_ERA = 40
COUNTRY_MAX_LEN = 255
STREET_MAX_LEN = 255
HOUSE_NUMBER_MAX_LEN = 8

class Country(UUIDMixin, models.Model):
    name = models.CharField(
        _('country'),
        max_length=COUNTRY_MAX_LEN,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = '"museum_data"."country"'
        verbose_name = _('country')
        verbose_name_plural = _('countries')


class City(UUIDMixin, models.Model):
    country = models.ForeignKey(
        Country, 
        verbose_name=_('country'),
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name = _('name'),
        max_length = MAX_LENGTH_NAME
    )

    def __str__(self) -> None:
        return f'{self.name}, {self.country}'

    class Meta:
        db_table = '"museum_data"."city"'
        verbose_name = _('city')
        verbose_name_plural = _('cities')
        unique_together = (
            (
                'name',
                'country',
            ),
        )


class Address(UUIDMixin, models.Model):
    city = models.ForeignKey(
        City,
        verbose_name=_('city'),
        on_delete=models.CASCADE
    )
    street = models.CharField(
        _('street name'),
        max_length=STREET_MAX_LEN,
        validators=[street_name_validator]
    )
    house_number = models.CharField(
        _('house number'),
        max_length=HOUSE_NUMBER_MAX_LEN,
        validators=[house_number_validator]
    )
    entrance_number = models.SmallIntegerField(
        _('entrance number'),
        null = True,
        blank = True,
    )
    floor = models.SmallIntegerField(
        _('floor number'),
        null = True,
        blank = True,
    )
    flat_number = models.SmallIntegerField(
        _('flat number'),
        null = True,
        blank = True,
    )

    def __str__(self) -> str:
        not_null_part = ' '.join([self.city.name, self.street, self.house_number])
        can_be_null_parts = ' '.join(
            [
                str(self.entrance_number),
                str(self.floor),
                str(self.flat_number)
            ]
        )        
        return f'{not_null_part} {can_be_null_parts}'.strip()

    class Meta:
        db_table = '"museum_data"."address"'        
        verbose_name = _('address')
        verbose_name_plural = _('addresses')
        unique_together = (
            (
                'city',
                'street',
                'house_number', 
                'entrance_number',
                'floor',
                'flat_number',
            ),
        )

class Museum(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.TextField(max_length=MAX_LENGTH_TITLE, verbose_name=_("title"))
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    rating = models.FloatField(verbose_name=_("rating"))

    def __str__(self) -> str:
        return self.title
    
    def check_positive(rating) -> None:
        if rating < 0:
            raise ValidationError('value should be equal or greater than zero')

    class Meta:
        db_table = '"museum_data"."museum"'
        unique_together = [['title', 'address']]
        verbose_name = _("museum")
        verbose_name_plural = _("museums")

class Guide(UUIDMixin, CreatedMixin, ModifiedMixin):
    firstname = models.TextField(max_length=MAX_LENGTH_NAME, verbose_name=_("first name"))
    lastname = models.TextField(max_length=MAX_LENGTH_NAME, verbose_name=_("last name"))
    birthday = models.DateField(verbose_name=_("birthday"), validators=[check_birthday])

    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname}'

    class Meta:
        db_table = '"museum_data"."guide"'
        verbose_name = _("guide")
        verbose_name_plural = _("guides")

class Exhibition(UUIDMixin, CreatedMixin, ModifiedMixin):
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE)
    theme = models.TextField(max_length=MAX_LENGTH_TITLE, unique=True, verbose_name=_("theme"))
    floor = models.IntegerField(verbose_name=_("floor"), validators=[check_positive])
    info = models.TextField(verbose_name=_("information"))

    def __str__(self) -> str:
        return f'{self.theme} {self.floor}'
  
    class Meta:
        db_table = '"museum_data"."exhibition"'
        verbose_name = _("exhibition")
        verbose_name_plural = _("exhibitions")

class Exhibit(UUIDMixin, CreatedMixin, ModifiedMixin):
    exposition = models.ForeignKey(Exhibition, on_delete=models.CASCADE)
    title = models.TextField(max_length=MAX_LENGTH_TITLE, unique=True, verbose_name=_("title"))
    info = models.TextField(verbose_name=_("information"))
    era = models.IntegerField(verbose_name=_("era"))

    def __str__(self) -> str:
        return f'{self.exposition}'

    class Meta:
        db_table = '"museum_data"."exhibit"'
        verbose_name = _("exhibit")
        verbose_name_plural = _("exhibits")

class MuseumGuide(UUIDMixin, models.Model):
    museum = models.ForeignKey(Museum, on_delete=models.CASCADE)
    guide = models.ForeignKey(Guide, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.guide} --- {self.museum}'

    class Meta:
        db_table = '"museum_data"."museum_guide"'
        unique_together = [['museum', 'guide']]
        verbose_name = _("museum guide")
        verbose_name_plural = _("museum guides")


