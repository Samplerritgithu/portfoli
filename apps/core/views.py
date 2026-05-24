from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from apps.blog.models import BlogPost
from apps.contact.models import ContactMessage
from apps.portfolio.models import (
    Certification,
    Education,
    Experience,
    Project,
    SkillCategory,
)

from .models import AboutStat, ArchitectureDiagram, SiteSettings, TechBadge


@require_GET
def home(request):
    site = SiteSettings.get_active()
    context = {
        'site': site,
        'about_stats': AboutStat.objects.all(),
        'tech_badges': TechBadge.objects.filter(is_featured=True),
        'skill_categories': SkillCategory.objects.prefetch_related('skills'),
        'experiences': Experience.objects.filter(is_active=True),
        'featured_projects': Project.objects.filter(is_featured=True, is_active=True)[:6],
        'all_projects': Project.objects.filter(is_active=True),
        'architecture_diagrams': ArchitectureDiagram.objects.filter(is_active=True),
        'certifications': Certification.objects.filter(is_active=True),
        'education': Education.objects.filter(is_active=True).first(),
        'recent_posts': BlogPost.objects.filter(status='published').order_by('-published_at')[:3],
    }
    return render(request, 'pages/home.html', context)


@require_GET
@cache_control(max_age=86400)
def manifest(request):
    data = {
        'name': 'Shiva Shankar Chanda Portfolio',
        'short_name': 'SSC Portfolio',
        'description': 'Full Stack Software Engineer Portfolio',
        'start_url': '/',
        'display': 'standalone',
        'background_color': '#0a0e17',
        'theme_color': '#6366f1',
        'icons': [
            {'src': '/static/images/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
            {'src': '/static/images/icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
        ],
    }
    return JsonResponse(data)


@require_GET
@cache_control(max_age=86400)
def service_worker(request):
    sw_content = """
const CACHE_NAME = 'ssc-portfolio-v1';
const ASSETS = ['/', '/static/css/main.css', '/static/js/main.js'];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE_NAME).then((c) => c.addAll(ASSETS)));
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((r) => r || fetch(e.request))
  );
});
"""
    return HttpResponse(sw_content, content_type='application/javascript')


def health_check(request):
    return JsonResponse({'status': 'ok'})
