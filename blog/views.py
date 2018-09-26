from datetime import datetime, timedelta, time

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum, Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# Create your views here.
from blog.forms import ArticleForm
from blog.models import Article, PageCount, Category
from hitcount.models import HitCount
from hitcount.views import HitCountMixin

today = datetime.now().date()
tomorrow = today + timedelta(1)
today_start = datetime.combine(today, time())
today_end = datetime.combine(tomorrow, time())


def blog_list(request):
    search = False
    object_list = Article.published.all().filter(trashed=False)
    all_object_list_count = Article.published.all().filter(trashed=False).count
    object_list_count = object_list.count()
    # today = timezone.now().date()

    cat_id = ""
    cat = request.GET.get("category")
    if cat:
        object_list = Article.published.all().filter(trashed=False).filter(category=cat)
        cat_id = int(cat)

    query = request.GET.get("q")
    if query:
        object_list = object_list.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
        object_list_count = object_list.count()
        search = True

    featured_articles = Article.published.all().filter(trashed=False).filter(featured=True)[0:5]

    order = "-publish_date"
    if request.method == 'POST':
        if request.POST.get("order_by_ac_date"):
            order = "-publish_date"
        elif request.POST.get("order_by_dc_date"):
            order = "publish_date"

        object_list = object_list.order_by(order)

    paginator = Paginator(object_list, 4)  # number of posts in each page
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        articles = paginator.page(1)
    except EmptyPage:
        # if page is out of range deliver last page of results
        articles = paginator.page(paginator.num_pages)

    # This code is using for hitcount on HomeScreen
    homescreen = PageCount.objects.get(page_name="home")
    hit_count = HitCount.objects.get_for_object(homescreen)
    homescreen_hit_count_response = HitCountMixin.hit_count(request, hit_count)

    homescreen_hit_count = homescreen.hit_count.hits

    # Total Count
    articles_hitcounts = Article.objects.all().aggregate(Sum('hit_count_generic__hits'))['hit_count_generic__hits__sum']

    # total_hitcounts = articles_hitcounts + homescreen_hit_count

    return render(request, 'blog/post/list.html', {'articles': articles,
                                                   # 'total_hitcounts': total_hitcounts,
                                                   'articles_hitcount': articles_hitcounts,
                                                   'articles_count': object_list_count,
                                                   'all_articles_count': all_object_list_count,
                                                   'featured_articles': featured_articles,
                                                   'search': search,
                                                   'cat_id': cat_id,
                                                   'categories': Category.objects.all()})


def blog_detail(request, year, month, day, slug):
    article = get_object_or_404(Article, slug=slug,
                                status='published',
                                publish_date__year=year,
                                publish_date__month=month,
                                publish_date__day=day, )
    hit_count = HitCount.objects.get_for_object(article)
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    hit_count = hit_count.hits
    return render(request, 'blog/post/detail.html', {'article': article,
                                                     'hit_count': hit_count})
