from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from activity.models import Activity
from product.models import Product


@csrf_exempt
def del_favorite(request):

    id = request.POST.get('id', None)
    Activity.objects.filter(content_type__app_label='product', content_type__model='product', object_id=id).delete()
    data = {
        'message': 'از لیست علاقه مندی حذف شد'
    }
    return JsonResponse(data)

@csrf_exempt
def del_p(request):
    id = request.POST.get('id', None)
    Product.objects.filter(id=id).delete()
    data={
        'message' : 'محصول با مفقیت حذف شد'
    }
    return JsonResponse(data)