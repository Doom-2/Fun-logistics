from django.contrib import admin
from .models import Order
from .tasks import get_orders
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME


@admin.action(description='Load data from spreadsheet')
def load_orders(modeladmin, request, queryset):
    get_orders.delay()


class OrderAdmin(admin.ModelAdmin):
    """
    Displays all fields in admin panel except 'id'.
    Allows only get data.
    Has action to load data from spreadsheet
    """

    list_display = ('seq_num', 'order', 'price_usd', 'price_rub', 'required_date',)
    list_display_links = ('order',)
    search_fields = ('order',)
    ordering = ('seq_num',)
    actions = (load_orders,)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=Order):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        """Allows call admin panel actions without selecting objects"""

        if 'action' in request.POST and request.POST['action'] == 'load_orders':
            if not request.POST.getlist(ACTION_CHECKBOX_NAME):
                post = request.POST.copy()
                for u in Order.objects.all():
                    post.update({ACTION_CHECKBOX_NAME: str(u.id)})
                request._set_post(post)
        return super(OrderAdmin, self).changelist_view(request, extra_context)


admin.site.register(Order, OrderAdmin)
