from rest_framework import routers
from .views import OrderViewSet

router = routers.SimpleRouter()
router.register('order', OrderViewSet)

urlpatterns = []
urlpatterns += router.urls
