from django.contrib import admin
from .exchange_rate_service import USD_RATE
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    """
    Displays all fields in admin panel except 'id'.
    Allows only get data.
    """
    readonly_fields = ('seq_num', 'order', 'price_usd', 'price_rub', 'required_date',)
    list_display = ('seq_num', 'order', 'price_usd', 'price_rub', 'required_date',)
    list_display_links = ('order',)
    search_fields = ('order',)
    ordering = ('seq_num',)

    def price_rub(self, obj: Order):
        if obj.price_usd and USD_RATE:
            return int(obj.price_usd * USD_RATE)
        else:
            return None

    price_rub.short_description = 'стоимость в руб.'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=Order):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Order, OrderAdmin)
