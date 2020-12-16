from django.contrib import admin

# Register your models here.
from .models import Product, ProductImage, Cart, CartItem, Checkout, UserStripe, EmailConfirmed, UserAddress

class UserAddressAdmin(admin.ModelAdmin):
    class Meta:
        model = UserAddress

admin.site.register(UserAddress, UserAddressAdmin)

#Some product details can be changed without looking inside
#Product can be found by searching or filtering 
class ProductAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    search_fields = ['title', 'description']
    list_display = ['title', 'price', 'active', 'updated']
    list_editable = ['price', 'active']
    list_filter = ['price', 'active']
    readonly_fields = ['updated', 'timestamp']
    prepopulated_fields = {"slug": ("title",)}
    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)

admin.site.register(ProductImage)

# Cart 
class CartAdmin(admin.ModelAdmin):
    class Meta:
        model = Cart

admin.site.register(Cart, CartAdmin)

admin.site.register(CartItem)

admin.site.register(Checkout)

admin.site.register(UserStripe)

admin.site.register(EmailConfirmed)
