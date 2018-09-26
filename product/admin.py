from django.contrib import admin

# Register your models here.
from product.models import Product, Type, Category, Field, Unit, ProductField, ProductPrice, ProductMedia

admin.site.register(Product)
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Field)
admin.site.register(ProductField)
admin.site.register(ProductPrice)
admin.site.register(ProductMedia)

