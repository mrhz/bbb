from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.utils import timezone
from hitcount.models import HitCount, HitCountMixin

from blog.forms import ArticleForm
from blog.models import Article, Category, Tag
from django.contrib.auth import get_user_model

User = get_user_model()


def dashboard_index(request):
    # Total posts count
    objects_count = Article.objects.all().count()
    objects_count_by_author = Article.objects.filter(author=request.user).count()

    # START Here! ( Total Hitcount )
    all_hitcount = Article.objects.all().aggregate(Sum('hit_count_generic__hits'))
    total_hitcount = all_hitcount["hit_count_generic__hits__sum"]
    # End Here

    # Start Here! ( total hitcount for author's Post )
    hit_count_for_author = Article.objects.filter(author=request.user).aggregate(Sum('hit_count_generic__hits'))
    author_posts_hitcounts = hit_count_for_author["hit_count_generic__hits__sum"]
    # End Here

    context = {'posts_count': objects_count,
               'author_posts_count': objects_count_by_author,
               'total_post_hitcount': total_hitcount,
               'author_posts_hitcounts': author_posts_hitcounts}
    return render(request, 'dashboard/blog/dashboard_index.html', context)


def all_blog_post_index(request):

    order = "-publish_date"
    number_of_shows = 15
    if request.method == 'POST':
        if request.POST.get("order_by_date"):
            order = "-publish_date"
        elif request.POST.get("order_by_author"):
            order = "author"
        elif request.POST.get("order_by_status"):
            order = "status"
        elif request.POST.get("order_by_title"):
            order = "title"

        # Code Below will change the number of post that shown in table
        if request.POST.get("number_of_shows_15"):
            number_of_shows = 15
        elif request.POST.get("number_of_shows_30"):
            number_of_shows = 30
        elif request.POST.get("number_of_shows_50"):
            number_of_shows = 50

        # Code below will move article to trash ( soft delete )
        if request.POST.get("object_id"):
            object_id = request.POST.get("object_id")
            obj = get_object_or_404(Article, id=object_id)
            obj.trashed = True
            obj.save()

    object_list = Article.objects.all().filter(trashed=False).order_by(order)


    paginator = Paginator(object_list, number_of_shows)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)




    return render(request, 'dashboard/blog/post_list.html', {'articles': articles,
                                                             'page': page,
                                                             "number_of_shows": number_of_shows,
                                                             'order': order})


def create_post(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)

            for tag in form.cleaned_data.get("tags"):
                instance.tags.add(tag)


            instance.author = request.user
            # # if request.user.is_authenticated():
            #     instance.author = request.user
            # else:
            #     # !!!!!!!!!!! make this better !!!!!!!!!!!!
            #     raise Http404
            if request.POST.get("submit_btn"):
                 instance.status = "published"
            elif request.POST.get("draft_btn"):
                instance.status = "draft"
            elif request.POST.get("archive_btn"):
                instance.status = "archived"

            instance.save()
            messages.success(request, "با موفقیت ثبت شد.", extra_tags='html_safe')
        else:
            messages.error(request, "خطا! متاسفانه به دلیل بروز خطا ویرایش انجام نگرفت")
    else:
        form = ArticleForm()
    return render(request, 'dashboard/blog/post_create.html', {'form': form,
                                                               'categories': Category.objects.all(),
                                                               'tags': Tag.objects.all()})


def post_edit(request, pk):
    instance = get_object_or_404(Article, pk=pk)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)

            instance.tags.clear()
            for tag in form.cleaned_data.get("tags"):
                instance.tags.add(tag)

            if request.POST.get("archive_btn"):
                    instance.status = "archived"
            elif request.POST.get("hidden_btn"):
                    instance.status = "hidden"


                # for ins_tag in instance.tags.all():
                #     if ins_tag not in form.cleaned_data.get("tags"):
                #         instance.tags.remove(ins_tag)

            instance.last_update = timezone.now()
            if request.POST.get("delete_btn"):
                instance.trashed = True
            instance.save()

            messages.success(request, " با موفقیت ویرایش یافت.", extra_tags='html_safe')
        else:
            messages.error(request, "خطا! متاسفانه به دلیل بروز خطا ویرایش انجام نگرفت.")
    return render(request, 'dashboard/blog/post_edit.html', {"title": instance.title,
                                                             "instance": instance,
                                                             'categories': Category.objects.all(),
                                                             'tags': Tag.objects.all(),
                                                             "form": form, })


def post_delete(request, year, month, day, slug):
    instance = get_object_or_404(Article, slug=slug,
                                 status='published',
                                 publish_date__year=year,
                                 publish_date__month=month,
                                 publish_date__day=day, )
    if request.method == 'POST':
        instance.delete()
        messages.success(request, "Deleted!")
        return redirect('blog:blog_list')
    return render(request, "dashboard/blog/delete.html", {'instance': instance})
