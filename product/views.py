from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
from buildino.settings import MEDIA_URL
from product.models import Product, Field, ProductField, Unit, Type, ProductPrice, ProductMedia, Category
from provider.models import Agency, Brand




@login_required()
def add_product(request):
    agency = Agency.objects.filter(user=request.user, status="accepted")
    units = Unit.objects.all()
    types = Type.objects.all()

    if request.method == "POST" and request.FILES["p_image"]:
        product = Product.objects.create(reseller_id=request.POST.get("reseller_brand"),
                                         type_id=request.POST.get("type_select"), unit_id=request.POST.get("units"), description=request.POST.get('desc'))
        product_price = ProductPrice.objects.create(product=product, proposed_by_id=request.POST.get('agency'))
        product_image = ProductMedia.objects.create(product=product, img=request.FILES['p_image'])
        fields_id = request.POST.getlist("input_fields")
        for f_id in fields_id:
            product_field = ProductField.objects.create(product=product, field_id=f_id)
            product_field.set_field_value(request.POST.get('field_input_' + str(f_id)))
            product_field.save()

        product_price.price = request.POST.get("p_price")
        product.name = request.POST.get("p_name")

        product_image.save()
        product_price.save()
        product.save()

        messages.success(request, "با موفقیت ثبت شد.", extra_tags='html_safe')

    return render(request, "profile/add_product.html", {"agency": agency,
                                                        "units": units,
                                                        "types": types})

def product(request):
    products = Product.objects.all()

    for product in products:
        print(product.name)
        for f in product.productfield_set.all():
            print(f.field.name + ": " + str(f.product_field))

    return render(request, 'buildino/product/product.html')

def product_list(request):
    type_value = request.POST.get('type', 0)
    brand_value = ''
    product = Product.objects.all()
    if request.method == 'POST':
        if 'type' in request.POST:
            if type_value == '0':
                product = Product.objects.all()
            else:
                product = product.filter(type_id=type_value)
        if 'brand' in request.POST:
            brand_value = request.POST.getlist('brand')
            for b in brand_value:
                if b:
                    product = product.filter(reseller__brand_id=b)

    type = Type.objects.all()
    brand = Brand.objects.all()
    return render(request, 'search.html',
                  {'product': product, 'type': type, 'type_value': int(type_value), 'brand': brand})

def product_detail(request, pk):
    products = Product.objects.filter(id=pk)
    products = products.get()
    pmedia = ProductMedia.objects.filter(product_id=pk)
    product_field = ProductField.objects.filter(product_id=products.id)
    all_product = Product.objects.all().order_by('-create_date')
    return render(request , 'product_detail.html',{'product':products, 'pmedia':pmedia, 'MEDIA_URL':MEDIA_URL,
                                                   'product_field': product_field, 'all_product':all_product})


def product_comparison(request):
    category = Category.objects.all()
    return render(request, 'comparison.html', {'category': category})