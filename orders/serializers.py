from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('seq_num', 'order', 'price_usd', 'price_rub', 'required_date')
