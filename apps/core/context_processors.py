from django.conf import settings

from .models import SiteSettings


def site_context(request):
    site = SiteSettings.get_active()
    return {
        'site': site,
        'github_url': settings.GITHUB_URL,
        'linkedin_url': settings.LINKEDIN_URL,
        'contact_email': settings.CONTACT_EMAIL,
    }
