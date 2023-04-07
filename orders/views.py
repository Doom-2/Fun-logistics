from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import renderers
from .models import Order
from .serializers import OrderSerializer
from .tasks import get_orders
from django.db.models import Sum


@api_view(['GET'])
@permission_classes((AllowAny,))
def health_check(request):
    """
    Healthcheck for this API in Docker container
    """
    return Response({'status': 'Ok'})


class OrderViewSet(ModelViewSet):
    """
    CRUD for Order model. Allows only get data.
    """

    queryset = Order.objects.all()
    http_method_names = ['get']
    serializer_class = OrderSerializer
    renderer_classes = (renderers.JSONRenderer, renderers.TemplateHTMLRenderer)

    def list(self, request, *args, **kwargs):
        """
        Gets order list, renders html template
        with <Orders> table, total order prices in USD
        and list of lists for pairs <required_date-sum(price_usd)>.
        Last one passes to Goggle Chart as rows data
        """

        get_orders.delay()
        response = super(OrderViewSet, self).list(request, *args, **kwargs)

        # calculate sum of <price_usd> column
        total_price_dict = Order.objects.aggregate(Sum('price_usd'))
        total_price = total_price_dict['price_usd__sum']

        # remove trailing zeros from <total_price> var if possible
        if total_price and int(total_price) == float(total_price):
            total_price = int(total_price)
        elif not total_price:
            total_price = None
        else:
            total_price = float(total_price)

        orders = Order.objects.all()

        date_price_tuples = list(
            Order.objects.all().filter(required_date__isnull=False, price_rub__isnull=False).values_list(
                'required_date').order_by('required_date').annotate(
                sum=Sum('price_usd')))
        date_price_list = [list(ele) for ele in date_price_tuples]

        if request.accepted_renderer.format == 'html':
            return Response({'orders': orders, 'total_price': total_price, 'date_price_list': date_price_list},
                            template_name='orders/orders.html')
        return response

    def retrieve(self, request, *args, **kwargs):
        """Gets single order"""

        get_orders.delay()

        return super().retrieve(request, *args, **kwargs)
