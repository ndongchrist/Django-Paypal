from django.contrib import admin

from store.models import Order, Product, Transaction
from paypal.standard.ipn.models import PayPalIPN

# Register your models here.
admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(Order)
