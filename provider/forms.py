from django import forms

from accounts.models import Address
from provider.models import Agency, Brand


class AgencyForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ('name','description', 'logo', 'commercial_code')


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('address', 'postal_code', 'phone_number', 'description',)


class BrandForm(forms.ModelForm):


    class Meta:
        model = Brand
        fields = ('name', 'logo', 'id_code', 'license_number','country')