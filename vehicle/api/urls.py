from django.urls import path, include
from rest_framework.routers import DefaultRouter

from vehicle.api import views as va

router = DefaultRouter()
router.register(r"vehicle-types", va.VehicleTypeAPIView)
router.register(r"vehicle", va.VehicleAPIView)


urlpatterns = [

    #path("locations-map/list/", mv.MapListAPIView.as_view()),

    path("", include(router.urls)),


]

