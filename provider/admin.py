from django.contrib import admin

# Register your models here.
from provider.models import Brand, Agency, Reseller, Standard

admin.site.register(Brand)
admin.site.register(Agency)
admin.site.register(Reseller)
admin.site.register(Standard)