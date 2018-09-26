from django.shortcuts import render

# Create your views here.
from accounts.models import Profile
from blog.models import Article
from product.models import Product
from provider.models import Brand


def index_view(request):

    profile_image = None
    if request.user.is_authenticated == True:
        profile = Profile.objects.get(user=request.user)
        profile_image = profile.profile_image

    brands = Brand.objects.filter(status="accepted")[0:8]
    products = Product.objects.all()[0:4]
    articles = Article.published.all()[0:4]


    return render(request,"buildino/index.html", {'products':products,
                                                  'brands': brands,
                                                  'articles': articles,
                                                  'profile_image': profile_image
                                                  })