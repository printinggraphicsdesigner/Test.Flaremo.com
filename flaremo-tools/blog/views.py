from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def blog_list(request):
    request.page_slug = 'blog'
    posts = BlogPost.objects.all()
    return render(request, 'blog/list.html', {'posts': posts})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blog/detail.html', {'post': post})