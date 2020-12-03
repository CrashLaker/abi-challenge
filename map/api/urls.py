from django.urls import path, include
from rest_framework.routers import DefaultRouter

from map.api import views as mv

router = DefaultRouter()
router.register(r"locations", mv.LocationViewSet)
router.register(r"locations-map", mv.MapViewSet)

app_name = 'location'

urlpatterns = [

    path("locations-map/list/", mv.MapListAPIView.as_view()),

    path("", include(router.urls)),

]

urlpatterns += router.urls

