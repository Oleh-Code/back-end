from django.db import models
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer


class Pizza(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    kkal = models.IntegerField()
    weight = models.IntegerField()
    photo = models.ImageField(upload_to='pizzas/')
    price = models.IntegerField()
    avaible = models.BooleanField(default=False)
    slug = models.SlugField(max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Pizza'
        verbose_name_plural = 'Pizzas'
        ordering = ['name']


class Order(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, default='')
    pizza_name = models.CharField(max_length=120, blank=True, null=True)
    pizza_img = models.ImageField(max_length=120, blank=True, null=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total = models.IntegerField(default=None, blank=True, null=True)

    def __str__(self):
        return self.pizza.name

    def save(self, *args, **kwargs):
        price = self.pizza.price
        self.pizza.price = price
        print(self.quantity)

        self.total = int(self.quantity) * price
        super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def __unicode__(self):
        return self.user

    def add_to_cart(self, product_slug):
        product = Pizza.objects.get(slug=product_slug)
        try:
            preexisting_order = Order(product=product, cart=self)
            preexisting_order.quantity += 1
            preexisting_order.save()
        except Order.DoesNotExist:
            new_order = Order.objects.create(
                product=product, cart=self, quantity=1)
            new_order.save()

            def __unicode__(self):
                return self.product_slug

    def remove_from_cart(self, pizza_slug):
        pizza = Pizza.objects.get(slug=pizza_slug)
        try:
            preexisting_order = Order.objects.get(pizza=pizza, cart=self)
            if preexisting_order.quantity > 1:
                preexisting_order.quantity -= 1
                preexisting_order.save()
            else:
                preexisting_order.delete()
        except Order.DoesNotExist:
            pass

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
