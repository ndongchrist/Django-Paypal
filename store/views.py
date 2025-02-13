import json

from django.shortcuts import render
# Create your views here.
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product
from django.shortcuts import get_object_or_404, render
from .models import Product, Order
from paypal.standard.forms import PayPalPaymentsForm
from .models import Transaction

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def checkout(request):
    # Retrieve cart data from local storage (simulated here)
    cart_data = request.session.get('cart', [])

    if not cart_data:
        return redirect('cart')  # Redirect to the cart page if the cart is empty

    # Create orders for each item in the cart
    orders = []
    total_amount = 0

    for item in cart_data:
        product = get_object_or_404(Product, id=item['id'])
        order = Order.objects.create(
            product=product,
            quantity=item['quantity'],
            total_price=float(item['price']) * item['quantity']
        )
        orders.append(order)
        total_amount += order.total_price

    # Generate PayPal payment form for the total amount
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": total_amount,
        "item_name": f"Cart Order ({len(orders)} items)",
        "invoice": f"CART-ORDER-{orders[0].id}",  # Use the first order ID as the invoice ID
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return_url": request.build_absolute_uri(reverse('payment_done')),
        "cancel_return": request.build_absolute_uri(reverse('payment_cancelled')),
    }

    form = PayPalPaymentsForm(initial=paypal_dict)

    # Clear the cart after generating the PayPal form
    request.session['cart'] = []

    return render(request, 'store/checkout.html', {'form': form, 'total_amount': total_amount})


def payment_done(request):
    return render(request, 'store/payment_done.html')

def payment_cancelled(request):
    return render(request, 'store/payment_cancelled.html')


from django.shortcuts import render
from django.http import JsonResponse
import json

def cart(request):
    if request.method == 'POST':
        # Retrieve cart data from the request body
        cart_data = json.loads(request.body).get('cart', [])
        request.session['cart'] = cart_data  # Save cart data in the session
        return JsonResponse({'success': True})

    # Retrieve cart data from the session
    cart_data = request.session.get('cart', [])
    cart_items = []

    # Calculate total items and total price
    total_items = 0
    total_price = 0

    for item in cart_data:
        total_items += item['quantity']
        total_price += float(item['price']) * item['quantity']
        cart_items.append({
            'id': item['id'],
            'name': item['name'],
            'price': item['price'],
            'quantity': item['quantity'],
            'total_price': float(item['price']) * item['quantity']
        })

    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'total_price': total_price
    }
    return render(request, 'store/cart.html', context)