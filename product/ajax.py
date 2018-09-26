from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from activity.models import Activity
from product.models import Field, Type, Product, ProductField
from provider.models import Brand, Reseller


@csrf_exempt
def add_field(request):
    if request.method == "POST":
        type = request.POST.get("type_id")
        fields = Field.objects.filter(type_field=type)
        fields_list = []
        for f in fields:
            fields_list.append({"id": f.id, "name": f.name, "type": f.type_choice, })

        print(fields_list
              )
        return JsonResponse({
            'message': "Its worked!",
            'fields': fields_list
        })
    else:
        response = JsonResponse({
            'error': "Internal ERROR!"
        })
        response.status_code = 403  # To announce that the user isn't allowed to publish
        return response


@csrf_exempt
def load_cat(request):
    if request.method == 'POST':
        cat = request.POST.get('cat', None)
        type = Type.objects.filter(category=cat).all()
        type_list = []
        for t in type:
            type_list.append({"id": t.id, "name": t.name})
        data = {
            'type': type_list
        }
        return JsonResponse(data)
    else:
        data = {
            'message': 'Error'
        }
        return JsonResponse(data)

@csrf_exempt
def load_product(request):
    if request.method == 'POST':
        type = request.POST.get('type', None)
        product = Product.objects.filter(type_id=type).all()
        fields = Field.objects.filter(type_field_id=type)
        product_list = []
        field_list = []
        for p in product:
            product_list.append({"id": p.id, "name": p.name})

        for f in fields:
            field_list.append({"id": f.id, "name": f.name})

        data = {
            'product': product_list,
            'field': field_list
        }
        return JsonResponse(data)
    else:
        data = {
            'message': 'Error'
        }
        return JsonResponse(data)

@csrf_exempt
def add_compare(request):
    if request.method == 'GET':
        product_id = request.GET.get('product',None)
        product = Product.objects.filter(id=product_id).get()
        product_detail = []
        field = ProductField.objects.filter(product_id=product_id)
        product_field = []
        product_detail.append({"id": product.id, "name": product.name, "price":product.productprice_set.first().price, "brand":product.reseller.brand.name, "unit":product.unit.name , 'image':product.productmedia_set.first().img.url})

        for f in field:
            product_field.append({'name': f.field.name, 'value':f.product_field})
        data = {
            'product': product_detail,
            'f_value':product_field
        }
        return JsonResponse(data)
    else:
        data = {
            'message': 'Error'
        }
        return JsonResponse(data)



@csrf_exempt
def search_field(request):
    if request.method == 'POST':
        product = ''
        value = request.POST.get('value', None)
        product = Product.objects.filter(name__contains=value).all()
        product_list = []
        for p in product:
            product_list.append({'id':p.id, 'name':p.name, 'price':p.productprice_set.first().price, 'image':p.productmedia_set.first().img.url})
        data={
            'product' : product_list
        }
        return JsonResponse(data)


@csrf_exempt
def search_filtering(request):
    product = Product.objects
    value = request.GET.getlist('brand[]')
    available = request.POST.getlist('value[]')
    cat = request.GET.get('cat', None)
    min_p = request.GET.get('min-p', None)
    max_p = request.GET.get('max-p', None)
    if available:
        for v in available:
            product = product.filter(is_available=v)
    if value:
        product = product.filter(reseller__brand_id__in=value)
    if cat != '0':
        product = product.filter(type_id=cat)
    if min_p:
        product = product.filter(productprice__price__range=(min_p, max_p))
    else:
        product= product.all()
    for p in product:
        print(p.name)
    product_list = []
    for p in product:
        product_list.append({'id': p.id, 'name': p.name, 'price': p.productprice_set.first().price,
                             'image': p.productmedia_set.first().img.url})
    data = {
        'product': product_list,
    }
    return JsonResponse(data)

@csrf_exempt
def favorite(request):
    message = ''
    id = request.POST.get('pk', None)
    product = Product.objects.get(pk=id)
    counter = product.favorite.count()
    if counter !=0:
        message = 'کالا تکراری است'
    else:
        product.favorite.create(activity_type=Activity.FAVORITE, user=request.user)
        message = 'با موفقیت به علاقه مندی ها اضافه شد!'
    data={
        'message': message
    }
    return JsonResponse(data)

@csrf_exempt
def load_brand(request):
    agency = request.POST.get('agency', None)
    brand_list = []
    brand = Reseller.objects.filter(type="master_agent" or "import_agent", brand__status="accepted", agency_id=agency)
    for b in brand:
        brand_list.append({'id': b.id, 'name': b.brand.name})
    data={
        'brands':brand_list
    }
    return JsonResponse(data)