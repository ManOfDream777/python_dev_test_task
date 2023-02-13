from datetime import datetime
from django.db import models
import random

class Item(models.Model):
    currencies = (
        ('usd', 'USD'),
        ('rub', 'RUB'),
    )
    name = models.CharField(verbose_name='Название товара', max_length=256)
    description = models.TextField(verbose_name='Описание товара')
    price = models.IntegerField(verbose_name='Цена товара', default=0)
    currency = models.CharField(choices=currencies, verbose_name='Валюта', max_length=3, default='')

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    items = models.ManyToManyField(Item, verbose_name='Товары')

    def __str__(self) -> str:
        return f'Заказ №{self.id}'

    def total(self) -> int:
        total = 0

        for item in self.items.all():
            total += item.price

        return total

class Discount(models.Model):
    """
        Accordingly this documentation https://stripe.com/docs/api/discounts/object 
    """
    discount_coupon = models.IntegerField(verbose_name='Скидка', help_text='Измеряется в процентах')
    start = models.DateTimeField(verbose_name='Действует', auto_now=True)
    end = models.DateTimeField(verbose_name='Заканчивается', auto_now=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='discount_order', verbose_name='Заказ')

    def __str__(self) -> str:
        return f'{self.discount_coupon}'

    def as_dict(self) -> dict:
        return {'id': self.id, 'object': 'discount', 'coupon': {'id': random.randint(4000, 20000), 'object': 'coupon', 'created_at': self.start, 'currency': self.order.define_currency(), 'percent_off': self.discount_coupon}, 'end': self.end, 'start': self.start, 'subscription': self.order}

class Tax(models.Model):
    """
        Accordingly this documentation https://stripe.com/docs/api/tax_rates/object
    """
    tax = models.IntegerField(verbose_name='Налог', help_text='Измеряется в процентах')
    active = models.BooleanField(verbose_name='Активна ли', default=False)
    country = models.CharField(verbose_name='Код страны', help_text='Формат ISO3166', max_length=2, default='DE')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='tax_order')

    def __str__(self) -> str:
        return f'{self.tax}%'

    def as_dict(self) -> dict:
        return {'id': self.id, 'object': 'tax_rate', 'active': self.active, 'country': self.country, 'created': datetime.now(), 'percentage': self.tax}