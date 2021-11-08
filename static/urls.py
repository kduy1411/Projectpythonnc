
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from mydrone import views

router = routers.DefaultRouter()
router.register(r'drones', views.DroneViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('mydrone.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('api/', include(router.urls)),
    path('orders/', include('orders.urls', namespace='orders')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]+static(settings.MEDIA_URL,
         document_root=settings.MEDIA_ROOT)
