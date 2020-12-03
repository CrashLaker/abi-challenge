from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order.api import views as ov

router = DefaultRouter()
router.register(f"order", ov.OrderViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("order/<int:pk>/vehicle/ranking", ov.ScoreViewSet.as_view()),
]
