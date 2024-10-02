from django.contrib import admin
from .models import Product, Cart, OrderItem, Order, Category, Supplier, SupplierOrder, UserProfile

# Register UserProfile and Product, Cart, OrderItem models directly
admin.site.register(UserProfile)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(OrderItem)

# Custom admin configuration for Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Your admin configuration here
    pass

# Custom admin configuration for Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    list_filter = ['parent']
    search_fields = ['name']

# Register other models as needed, making sure not to use decorators again for those already registered
admin.site.register(Supplier)
admin.site.register(SupplierOrder)
