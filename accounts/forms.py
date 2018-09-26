from .models import Profile

from django import forms


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    profile_image = forms.ImageField()

    class Meta:
        model = Profile
        fields = ('first_name','last_name','national_code','profile_image', 'gender')


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='نام')
    last_name = forms.CharField(max_length=30, label='نام خانوادگی')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()