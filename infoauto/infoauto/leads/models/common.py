# -*- coding: utf-8 -*-

from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

postal_code_regex = RegexValidator(
    regex=r'^\d{5}$',
    message=_("Postal Code must be entered in the format: '11111'. Up to 5 digits allowed."))

phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message=_("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
