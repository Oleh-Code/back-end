from rest_framework import serializers
from .models import Pizza, Order, Cart


class PizzaListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pizza
        fields = ('id', 'name', 'kkal', 'weight',
                  'price', 'photo', 'avaible', 'slug')


class PizzaDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pizza
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    pizza = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug'
    )

    class Meta:
        model = Order
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Cart
        fields = '__all__'
