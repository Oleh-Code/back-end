from django.urls import path
from . import views

urlpatterns = [
    path('', views.PizzaListAPIView.as_view(), name='pizza-list'),
    path('carts/', views.CartListAPIView.as_view(), name='carts-list'),
    path('orders/', views.OrderListAPIView.as_view(), name='order-list'),
    path('pizza/<slug:slug>/', views.PizzaDetailAPIView.as_view(), name='pizza-detail'),
    path('add-to-cart/<slug:pizza_slug>/',
         views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug:pizza_slug>/',
         views.remove_from_cart, name='remove-from-cart'),
    path('buy/', views.buy, name='buy'),
    path('add-from-detail/<slug:pizza_slug>/',
         views.createfnc, name='add-from-detail')
]
