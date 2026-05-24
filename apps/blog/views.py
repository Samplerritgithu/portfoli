from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET

from .models import BlogPost, Category, Tag
from .services import BlogService


@require_GET
def post_list(request):
    search = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    tag_slug = request.GET.get('tag', '')
    posts = BlogService.get_published_posts(search, category_slug, tag_slug)
    paginator = Paginator(posts, 6)
    page = paginator.get_page(request.GET.get('page', 1))
    return render(request, 'blog/list.html', {
        'page_obj': page,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'search': search,
        'active_category': category_slug,
        'active_tag': tag_slug,
    })


@require_GET
def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    BlogService.increment_views(post)
    rendered_content = BlogService.render_content(post)
    comments = post.comments.filter(is_approved=True, parent__isnull=True)
    return render(request, 'blog/detail.html', {
        'post': post,
        'rendered_content': rendered_content,
        'comments': comments,
        'related_posts': BlogPost.objects.filter(
            status='published', category=post.category
        ).exclude(pk=post.pk)[:3],
    })
