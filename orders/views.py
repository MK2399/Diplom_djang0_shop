import os

from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.core.mail import send_mail
from dotenv import load_dotenv

load_dotenv()


def order_create(request):
    cart = Cart(request)
    email = request.POST.get('email', '')
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                send_mail(subject='Ваш заказ',
                          message=f"Ваш заказ оформлен, {item['product']}, количество {item['quantity']},"
                                  f" сумма заказа {item['quantity'] * item['price']}. Спасибо, что выбрали нас!",
                          from_email=os.getenv('EMAIL_HOST_USER'), recipient_list=[order.email]
                          )
            cart.clear()
            return render(request, 'templates_orders/created_order.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'templates_orders/creat_order.html', {'cart': cart, 'form': form})