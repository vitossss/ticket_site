from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone


class Ticket(models.Model):
    name = models.CharField("Назва квитка", max_length=255)
    slug = models.SlugField("Slug", max_length=100, unique=True)
    price = models.DecimalField("Ціна квитка", max_digits=20, decimal_places=2)
    image = models.ImageField("Зображення квитка", upload_to="tickets/img/", blank=True, null=True)
    description = models.TextField("Опис квитка", blank=True, null=True)
    creation_time = models.DateTimeField("Дата створення квитка", auto_now_add=True)
    day = models.DateField("Дата проведення")
    time = models.TimeField("Час проведення")
    place = models.CharField("Місце проведення", max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Квиток"
        verbose_name_plural = "Квитки"
        ordering = ['pk']

    def __str__(self):
        return f'{self.name}, {self.price}'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField("Кількість", max_digits=20, decimal_places=2, blank=True, null=True)
    time = models.DateTimeField("Дата створення платежу", auto_now_add=True)
    comment = models.TextField("Коментар", blank=True, null=True)

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплата"
        ordering = ['pk']

    def __str__(self):
        return f'{self.user}, {self.time}'


class Order(models.Model):
    STATUS_CART = "1_cart"
    STATUS_WAITING_FOR_PAYMENT = "2_waiting_for_payment"
    STATUS_PAID = "3_paid"
    STATUS_CHOICES = [
        (STATUS_CART, 'cart'),
        (STATUS_WAITING_FOR_PAYMENT, 'waiting_for_payment'),
        (STATUS_PAID, 'paid')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_CART)
    amount = models.DecimalField("Кількість", max_digits=20, decimal_places=2, blank=True, null=True)
    creation_time = models.DateTimeField("Дата створення замовлення", auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, blank=True, null=True)
    comment = models.TextField("Коментар", blank=True, null=True)

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ['pk']

    def __str__(self):
        return f'{self.user}, {self.status}'

    @staticmethod
    def get_cart(user: User):
        cart = Order.objects.filter(user=user, status=Order.STATUS_CART).first()
        if cart and (timezone.now() - cart.creation_time).days > 7:
            cart.delete()
            cart = None
        if not cart:
            cart = Order.objects.create(user=user, status=Order.STATUS_CART, amount=0)
        return cart

    def get_amount(self):
        amount = Decimal(0)
        for item in self.orderitem_set.all():
            amount += item.amount
        return amount

    def make_order(self):
        items = self.orderitem_set.all()
        if items and self.status == Order.STATUS_CART:
            self.status = Order.STATUS_WAITING_FOR_PAYMENT
            self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Ticket, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField("Кількість", default=1)
    price = models.DecimalField("Ціна", max_digits=20, decimal_places=2)
    discount = models.DecimalField("Знижка", max_digits=20, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Квиток"
        verbose_name_plural = "Квитки в замовленні"
        ordering = ['pk']

    def __str__(self):
        return f'{self.order}, {self.price}'

    @property
    def amount(self):
        amount = self.quantity * (self.price - self.discount)
        return amount


@receiver(post_save, sender=OrderItem)  # Функція виконається після збереження об'єкта в OrderItem
def recalculate_order_amount(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()


@receiver(post_delete, sender=OrderItem)  # Функція виконається після збереження об'єкта в OrderItem
def recalculate_order_amount(sender, instance, **kwargs):
    order = instance.order
    order.amount = order.get_amount()
    order.save()
