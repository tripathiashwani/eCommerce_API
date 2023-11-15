
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from product import views
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
router=DefaultRouter()
router.register(r"category",views.categoryViewSet)
router.register(r"brand",views.brandViewSet)
router.register(r"product",views.productViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/schema', SpectacularAPIView.as_view(),name="schema"),
    path('api/schema/docs', SpectacularSwaggerView.as_view(url_name="schema")),
]
