from django.urls import path
from . import views

app_name = 'store'
urlpatterns = [
    path('' , views.index , name='index.html'),
    path('drone.html/<int:pk>/', views.drone_detail , name='drone.html'),
    path('shop.html/<int:pk>/', views.shop, name='shop.html'),
    path('cart.html' ,views.cart , name= 'cart.html'),
    path('register.html' , views.register , name= 'register.html'),
    path('login.html', views.log_in , name = 'login.html'),
    path('checkout.html' , views.checkout , name = 'checkout.html'),
    path('forget-password.html' , views.forgetpass,name='forget-password.html'),
    path('drones.html', views.read_drones, name='drones.html'),
    path('logout.html', views.log_out, name='logout.html'),
    path('price_filter.html' , views.filter_by_prices, name='price_filter.html'),
    path('search.html' ,views.search_form,name='search.html'),
]
