import zoneinfo
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Ticket, Payment, Order, OrderItem


class UnitTests(TestCase):
    fixtures = ["shop/fixtures/mydata.json"]

    def setUp(self):
        self.user = User.objects.get(username='root')
        self.ticket = Ticket.objects.all().first()

    def test_user_exists(self):
        """
        Перевірка чи існує юзер з правами адміністратора
        """
        users = User.objects.all()
        users_count = users.count()
        user = users.first()
        self.assertEqual(users_count, 1)  # Порівняння двох значень
        self.assertEqual(user.username, 'root')
        self.assertTrue(user.is_superuser)  # Перевірка значення True False

    def test_user_check_password(self):
        self.assertTrue(self.user.check_password('root'))

    # def test_all_data(self):
    #     self.assertGreater(Ticket.objects.all().count(), 0)
    #     self.assertGreater(Order.objects.all().count(), 0)
    #     self.assertGreater(OrderItem.objects.all().count(), 0)  # !Тест тимчасово зафейлений!
    #     self.assertGreater(Payment.objects.all().count(), 0)

    def find_cart_number(self):
        """
        Фукнція яка шукає номер корзини
        """
        cart_number = Order.objects.filter(user=self.user, status=Order.STATUS_CART).count()
        return cart_number

    def test_get_cart(self):
        """
        Функція яка взаємодіє з корзиною:
        1. Корзини не існує
        2. Додавання корзини
        3. Вернути попередньо створену корзину
        """
        # 1. Корзини не існує
        self.assertEqual(self.find_cart_number(), 0)
        # 2. Додавання корзини
        Order.get_cart(self.user)
        self.assertEqual(self.find_cart_number(), 1)
        # 3. Перевірка чи не створюється нова корзина
        Order.get_cart(self.user)
        self.assertEqual(self.find_cart_number(), 1)

    def test_cart_older_7_days(self):
        """
        Функція перевіряє чи корзина вже застаріла
        Корзина рахується застарілою коли спливає термін 7 днів
        """
        cart = Order.get_cart(self.user)
        cart.creation_time = timezone.datetime(2000, 1, 1, tzinfo=zoneinfo.ZoneInfo('UTC'))
        cart.save()
        cart = Order.get_cart(self.user)
        self.assertEqual((timezone.now() - cart.creation_time).days, 0)

    def test_recalculate_order_amount(self):
        """
        Функція перевіряє чи змінюється значення суми після видалення або додавання нового квитка
        Сума має перераховуватися автоматично
        """
        # 1. Корзина пуста
        cart = Order.get_cart(self.user)
        self.assertEqual(cart.amount, Decimal(0))
        # 2. Після додавання нового квитка
        item = OrderItem.objects.create(order=cart, product=self.ticket, price=2, quantity=2)
        item = OrderItem.objects.create(order=cart, product=self.ticket, price=2, quantity=3)
        cart = Order.get_cart(self.user)
        self.assertEqual(cart.amount, Decimal(10))
        # 3. Після видалення квитка
        item.delete()
        cart = Order.get_cart(self.user)
        self.assertEqual(cart.amount, Decimal(4))

    def test_cart_status_change(self):
        """
        Фукція перевіряє чи змінюється статус корзини
        """
        # 1. Зміна статусу при порожній корзині
        cart = Order.get_cart(self.user)
        cart.make_order()
        self.assertEqual(cart.status, Order.STATUS_CART)
        # 2. Зміна статусу при оплаті
        OrderItem.objects.create(order=cart, product=self.ticket, price=2, quantity=3)
        cart.make_order()
        self.assertEqual(cart.status, Order.STATUS_WAITING_FOR_PAYMENT)







