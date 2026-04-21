from blog.models import BlogPost

def dynamic_blogs(request):
    tool_slug = getattr(request, 'tool_slug', None)
    page_slug = getattr(request, 'page_slug', None)

    # Base queryset
    blogs = BlogPost.objects.filter(is_published=True)

    # 👉 Tool ভিত্তিক blog
    if tool_slug:
        blogs = blogs.filter(tool__slug=tool_slug)

    # 👉 Page ভিত্তিক blog
    elif page_slug:
        blogs = blogs.filter(page=page_slug)

    # 👉 Global blog
    else:
        blogs = blogs.filter(tool__isnull=True, page__isnull=True)

    # 👉 যদি কিছু না পাওয়া যায় → fallback global
    if not blogs.exists():
        blogs = BlogPost.objects.filter(
            is_published=True,
            tool__isnull=True,
            page__isnull=True
        )

    return {
        'dynamic_blogs': blogs.order_by('-created_at')[:5]
    }