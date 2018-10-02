from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from provider.forms import AgencyForm, AddressForm, BrandForm
from provider.models import Agency, Reseller, Brand

@csrf_exempt
@login_required
def upgrade_account(request):
    if request.method == 'POST':
        agency = Agency.objects.create(user=request.user)
        address = agency.address.create()

        agency_form = AgencyForm(request.POST, request.FILES, instance=agency)
        address_form = AddressForm(request.POST, instance=address)
        if agency_form.is_valid() and address_form.is_valid():
            a = agency_form.save(commit=False)
            b = address_form.save(commit=False)
            a.save()
            b.save()
            messages.success(request, "با موفقیت انجام شد.", extra_tags='html_safe')
        else:
            messages.error(request, "خطا! متاسفانه به دلیل بروز خطا عملیات انجام نگرفت")
    else:
        agency_form = AgencyForm()
        address_form = AddressForm()

    return render(request, 'metronic/add_shop_wizard.html', {'agency_form': agency_form,
                                                             'address_form': address_form})


@login_required
def submit_brand(request):
    try:
        agency = Agency.objects.get(user=request.user, status="accepted")

        if request.method == 'POST':
            brand, created = Brand.objects.create(owner=agency)
            brand_form = BrandForm(request.POST, instance=brand)
            if brand_form.is_valid():
                a = brand_form.save(commit=False)
                a.save()
                resseler, created = Reseller.objects.get_or_create(agency=agency, brand=brand, type="master_agent")
                messages.success(request, "با موفقیت انجام شد.", extra_tags='html_safe')
            else:
                messages.error(request, "خطا! متاسفانه به دلیل بروز خطا عملیات انجام نگرفت")
        else:
            brand_form = BrandForm()

    except:
        return HttpResponseNotFound("<h1>Sorry!</h1><h2> you dont have permission to do this! :(</h2>")

    return render(request, 'account/submit_brand.html', {
        'agency': agency,
        'brand_form': brand_form})


def brand_list(request):
    brand = Brand.objects.filter(owner__user=request.user)
    return render(request, 'brands.html', {'brand':brand})

def brand_detail(request, pk):
    brand = Brand.objects.filter(id=pk).get()
    return render(request, 'brand_detail.html', {'brand': brand})


@login_required
def edit_brand(request, id):
    agencies = Agency.objects.filter(user=request.user, status="accepted")
    instance = Brand.objects.filter(id=id)
    form = BrandForm(request.POST or None, request.FILES or None, instance)
    if request.method == 'POST':
        instance.update(name = request.POST.get('name'), owner_id=request.POST.get('agancy'), country=request.POST.get('country'), logo=request.FILES.get('logo'), id_code=request.POST.get('id_code'), license_number=request.POST.get('license_number'))
        return redirect('accounts:profile')
    return render(request, 'account/edit_brand.html', {'brand':instance.get(), 'agencies':agencies})