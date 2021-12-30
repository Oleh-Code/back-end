from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import permissions
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Order, Pizza, Cart
from .serializers import OrderSerializer, PizzaListSerializer, PizzaDetailSerializer, CartSerializer
from .service import PaginationModel


class PizzaListAPIView(ListAPIView):
    pagination_class = PaginationModel
    serializer_class = PizzaListSerializer
    queryset = Pizza.objects.filter(avaible=True)


class PizzaDetailAPIView(RetrieveAPIView):
    serializer_class = PizzaDetailSerializer
    queryset = Pizza.objects.filter(avaible=True)
    lookup_field = 'slug'


class CartListAPIView(ListAPIView):
    pagination_class = PaginationModel
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class OrderListAPIView(ListAPIView):
    serializer_class = OrderSerializer
    pagination_class = PaginationModel
    permissions_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return Order.objects.filter(cart__user=self.request.user, cart__active=True)


@api_view(['GET', 'POST'])
def add_to_cart(request, pizza_slug):
    pizza = get_object_or_404(Pizza, slug=pizza_slug)
    print(pizza.photo)
    cart, created = Cart.objects.get_or_create(user=request.user, active=True)
    order, created = Order.objects.get_or_create(
        pizza=pizza, cart=cart, pizza_img=pizza.photo, pizza_name=pizza.name)
    order.quantity += 1
    order1 = order.save()
    serializer = OrderSerializer(order1, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def remove_from_cart(request, pizza_slug):
    pizza = get_object_or_404(Pizza, slug=pizza_slug)
    cart = Cart.objects.get(user=request.user, active=True)
    cart.remove_from_cart(pizza_slug)
    return Response({'ALL FINE'})


@api_view(['GET', 'POST'])
def buy(request):
    cart = Cart.objects.get(user=request.user, active=True)
    print(cart)
    cart.active = False
    cart.save()
    return Response({'All Fine, you bought'})


class CreateView(APIView):
    def post(self, request):
        model = OrderSerializer(data=request.data)
        if model.is_valid():
            model.save()
        return Response(status=201)


@api_view(['GET', 'POST'])
def createfnc(request, pizza_slug):
    print(request.data)
    pizza = get_object_or_404(Pizza, slug=pizza_slug)
    cart, created = Cart.objects.get_or_create(user=request.user, active=True)
    order, created = Order.objects.get_or_create(
        pizza=pizza, cart=cart, pizza_img=pizza.photo, pizza_name=pizza.name)
    order.quantity += request.data['quantity']
    order1 = order.save()
    serializer = OrderSerializer(order1, many=True)
    return Response(serializer.data)
