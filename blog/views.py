from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render,get_object_or_404

from comment.models import Comment
from read_statistics.utils import read_statistics_onece_read
from .models import Blog,BlogType
from django.core.paginator import Paginator # 分页器
from django.db.models import Count #计数
from comment.forms import CommentForm

# Create your views here.
'''
博客列表内容
'''
def blog_list(request):
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list,6)
    page_num = request.GET.get("page", 1)  # 获取url页面参数
    page_of_blogs = paginator.get_page(page_num)

    currentr_page_num = page_of_blogs.number  # 获取当前页码
    page_range = [x for x in range(currentr_page_num-2, currentr_page_num+3) if 0<x<=paginator.num_pages]
    # 加上省略号，首尾页
    if page_range[0] - 1 >= 2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1]>=2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    blog_dates = Blog.objects.dates('create_time','month',order='DESC')
    blog_dates_dict={}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['page_of_blogs'] = page_of_blogs # 当前页面的所有博客
    #context['blog_types'] = BlogType.objects.all()
    # blog_count为自己取的名字
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['page_range'] = page_range
    context['blog_dates'] = blog_dates_dict
    return render(request,'blog_list.html',context)


'''
博客标签分类，列表内容
'''
def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)

    paginator = Paginator(blogs_all_list, 6)
    page_num = request.GET.get("page", 1)  # 获取url页面参数
    page_of_blogs = paginator.get_page(page_num)

    currentr_page_num = page_of_blogs.number  # 获取当前页码
    page_range = [x for x in range(currentr_page_num - 2, currentr_page_num + 3) if 0 < x <= paginator.num_pages]
    # 加上省略号，首尾页
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    blog_dates = Blog.objects.dates('create_time','month',order='DESC')
    blog_dates_dict={}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['blog_type'] = blog_type
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return render(request,'blogs_with_type.html',context)


'''
博客日期分类，列表内容
'''
def blogs_with_date(request,year,month):

    blogs_all_list = Blog.objects.filter(create_time__year=year,create_time__month=month)
    paginator = Paginator(blogs_all_list, 6)
    page_num = request.GET.get("page", 1)  # 获取url页面参数
    page_of_blogs = paginator.get_page(page_num)

    currentr_page_num = page_of_blogs.number  # 获取当前页码
    page_range = [x for x in range(currentr_page_num - 2, currentr_page_num + 3) if 0 < x <= paginator.num_pages]
    # 加上省略号，首尾页
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    blog_dates = Blog.objects.dates('create_time','month',order='DESC')
    blog_dates_dict={}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    context['blog_with_date'] = '%s年%s月' % (year,month)
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    return render(request,'blogs_with_date.html', context)

'''
博客详情页面内容
'''
def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    key = read_statistics_onece_read(request,blog)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk,parent=None)

    context = {}
    context['blog'] = blog
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    context['comments'] = comments.order_by('-comment_time')
    # 数据初始化
    data={'content_type':blog_content_type.model,'object_id':blog_pk,'reply_comment_id': 0}
    context['comment_form'] = CommentForm(initial=data)

    response =  render(request,'blog_detail.html',context)
    response.set_cookie(key,'true')
    return response


