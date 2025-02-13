from django.urls import path, include
from store import views
from paypal.standard.ipn import urls as paypal_urls

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/<int:product_id>/', views.checkout, name='checkout_id'),
    path('paypal/', include(paypal_urls)),
    path('payment-done/', views.payment_done, name='payment_done'),
    path('payment-cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('cart/', views.cart, name='cart'),
]