from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

# Create your views here.
from accounts.forms import ProfileForm
from accounts.models import Profile
from product.models import Product
from provider.models import Agency, Brand


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'account/profile.html', {"profile": profile,
                                                    "user": request.user})


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    print(profile.gender)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('accounts:profile')

    return render(request, "account/edit_profile.html", {'form': form,
                                                         'profile': profile})

@login_required
def account_shop_status(request):
    try:
        agencies = Agency.objects.filter(user=request.user)
    except ObjectDoesNotExist:
        agencies = None

    return render(request,'account/shop_status.html',{'agencies':agencies})


@login_required
def account_brand_status(request):
    try:
        brands = Brand.objects.filter(owner__user=request.user)
    except ObjectDoesNotExist:
        brands = None

    return render(request,'account/brand_status.html',{'brands':brands})


@login_required
def favorite_list(request):
    try:
        favorites = Product.objects.filter(reseller__agency__user=request.user).exclude(favorite=None)
    except ObjectDoesNotExist:
        favorites = None

    return render(request,'account/favorite_list.html',{'favorites':favorites})
