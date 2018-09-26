from django.contrib import admin

# Register your models here.
from accounts.models import Profile, Phone_Number, Address

admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Phone_Number
                    )
