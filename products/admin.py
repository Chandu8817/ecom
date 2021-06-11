from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(ProductImages)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(BillingAddress)
admin.site.register(OrderDetail)


