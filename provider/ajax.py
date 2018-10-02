from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from provider.models import Agency


@csrf_exempt
def submit_shop(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        logo = request.POST.get('logo', None)
        commercial_code = request.POST.get('commercial_code', None)
        postal_code = request.POST.get('postal_code', None)
        address = request.POST.get('address', None)
        phone_number = request.POST.get('phone_number', None)
        description = request.POST.get('description', None)

        Agency.objects.create(user=request.user, name=name, logo=logo, description=description, commercial_code=commercial_code)
        data = {
            'message':'OK'
        }
        return JsonResponse(data)