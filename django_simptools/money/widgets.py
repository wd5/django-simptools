# -*- coding: UTF-8 -*-
'''
Created on May 7, 2011
@author: jake
@site: https://github.com/jakewins/django-money
'''
from django import forms
from moneyed.classes import Money, CURRENCIES, DEFAULT_CURRENCY
from decimal import Decimal
import operator

__all__ = ('InputMoneyWidget', 'CurrencySelectWidget',)

CURRENCY_CHOICES = [(c.code, c.name) for i, c in CURRENCIES.items() if c.code != DEFAULT_CURRENCY.code]
CURRENCY_CHOICES.sort(key=operator.itemgetter(1))

class CurrencySelectWidget(forms.Select):
    def __init__(self, attrs=None, choices=CURRENCY_CHOICES):
        super(CurrencySelectWidget, self).__init__(attrs, choices)

class InputMoneyWidget(forms.TextInput):

    def __init__(self, attrs=None, currency_widget=None):
        self.currency_widget = currency_widget or CurrencySelectWidget()
        super(InputMoneyWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        amount = ''
        currency = ''
        if isinstance(value, Money):
            amount = value.amount
            currency = value.currency.code
        if isinstance(value, tuple):
            amount = value[0]
            currency = value[1]
        if isinstance(value, int) or isinstance(value, Decimal):
            amount = value
        result = super(InputMoneyWidget, self).render(name, amount)
        result += self.currency_widget.render(name+'_currency', currency)
        return result

    def value_from_datadict(self, data, files, name):
        return (data.get(name, None), data.get(name+'_currency', None))
