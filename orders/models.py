from django.db import models


class Order(models.Model):
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    seq_num = models.BigIntegerField(verbose_name='№', null=True, blank=True, unique=True)
    order = models.BigIntegerField(verbose_name='заказ №', null=True, blank=True, unique=True)
    price_usd = models.FloatField(verbose_name='стоимость,$', null=True, blank=True, max_length=10)
    price_rub = models.BigIntegerField(verbose_name='стоимость в руб.', null=True, blank=True)
    required_date = models.DateField(verbose_name='срок поставки', null=True, blank=True, max_length=10)

    def __str__(self):
        return str(self.order)
