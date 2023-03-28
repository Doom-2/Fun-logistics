from django.db import models
from .exchange_rate_service import USD_RATE


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    seq_num = models.BigIntegerField(verbose_name='№', null=True, blank=True, unique=True)
    order = models.BigIntegerField(verbose_name='заказ №', null=True, blank=True, unique=True)
    price_usd = models.FloatField(verbose_name='стоимость,$', null=True, blank=True, max_length=10)
    required_date = models.DateField(verbose_name='срок поставки', null=True, blank=True, max_length=10)

    def __str__(self):
        return str(self.order)

    @property
    def price_rub(self):
        """Calculates order price in RUB according actual USD rate"""

        if self.price_usd and USD_RATE:
            return int(self.price_usd * USD_RATE)
        else:
            return None
