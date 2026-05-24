import markdown
from bleach import clean
from django.db.models import Q
from django.utils import timezone

from .models import BlogPost, Comment


ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'ul', 'ol', 'li', 'a', 'code', 'pre', 'blockquote', 'img',
]
ALLOWED_ATTRIBUTES = {'a': ['href', 'title'], 'img': ['src', 'alt']}


class BlogService:
    @staticmethod
    def render_content(post: BlogPost) -> str:
        if post.content_format == 'markdown':
            html = markdown.markdown(post.content, extensions=['fenced_code', 'tables'])
            return clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)
        return clean(post.content, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)

    @staticmethod
    def get_published_posts(search: str = '', category_slug: str = '', tag_slug: str = ''):
        qs = BlogPost.objects.filter(status='published').select_related('category', 'author').prefetch_related('tags')
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(content__icontains=search) | Q(excerpt__icontains=search))
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        if tag_slug:
            qs = qs.filter(tags__slug=tag_slug)
        return qs

    @staticmethod
    def increment_views(post: BlogPost):
        BlogPost.objects.filter(pk=post.pk).update(view_count=post.view_count + 1)

    @staticmethod
    def create_comment(post: BlogPost, data: dict) -> Comment:
        return Comment.objects.create(
            post=post,
            author_name=data['author_name'],
            author_email=data['author_email'],
            content=data['content'],
            parent_id=data.get('parent'),
        )

    @staticmethod
    def publish_post(post: BlogPost):
        post.status = 'published'
        if not post.published_at:
            post.published_at = timezone.now()
        post.save()
