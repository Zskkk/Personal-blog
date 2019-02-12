from django.shortcuts import render
from apps.models import Article, Category, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.conf import settings

categories = Category.objects.all()  # 获取全部的分类对象
tags = Tag.objects.all()  # 获取全部的标签对象


def home(request):  # 主页
    posts = Article.objects.all()  # 获取全部的Article对象
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list, 'category_list': categories, "tags": tags})


def detail(request, id):  # 文章详情页
    try:
        post = Article.objects.get(id=str(id))
        post.viewed()  # 更新浏览次数
        tags = post.tags.all()
        next_post = post.next_article()  # 上一篇文章对象
        prev_post = post.prev_article()  # 下一篇文章对象
    except Article.DoesNotExist:
        raise Http404
    return render(
        request, 'post.html',
        {
            'post': post,
            'tags': tags,
            'category_list': categories,
            'next_post': next_post,
            'prev_post': prev_post
        }
    )


def search_category(request, id):  # 分类搜索
    posts = Article.objects.filter(category_id=str(id))
    category = categories.get(id=str(id))
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'category.html', {'post_list': post_list, 'category_list': categories, 'category': category})


def search_tag(request, tag):  # 标签搜索
    posts = Article.objects.filter(tags__name__contains=tag)
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'tag.html', {'post_list': post_list, 'category_list': categories, 'tag': tag})



def search_article(request): #文章搜索
    if request.method == "POST":
        search = request.POST.get("search")
        if not search:
            error_msg = '内容不能为空'
            posts = Article.objects.all()  # 获取全部的Article对象
            paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM
            page = request.GET.get('page')  # 获取URL中page参数的值
            try:
                post_list = paginator.page(page)
            except PageNotAnInteger:
                post_list = paginator.page(1)
            except EmptyPage:
                post_list = paginator.page(paginator.num_pages)
            return render(request, 'home.html', {'post_list': post_list,
                                                 'category_list': categories,
                                                 'error_msg': error_msg})
        else:
            posts = Article.objects.filter(title__icontains=search)
            paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM
            page = request.GET.get('page')  # 获取URL中page参数的值
            try:
                post_list = paginator.page(page)
            except PageNotAnInteger:
                post_list = paginator.page(1)
            except EmptyPage:
                post_list = paginator.page(paginator.num_pages)
            return render(request, 'search_article.html', {'post_list': post_list, 'category_list': categories})
