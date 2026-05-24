from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(TimeStampedModel):
    THEME_CHOICES = [
        ('dark', 'Dark'),
        ('light', 'Light'),
        ('auto', 'Auto'),
    ]

    name = models.CharField(max_length=200, default='Shiva Shankar Chanda')
    title = models.CharField(max_length=200, default='Full Stack Software Engineer')
    location = models.CharField(max_length=200, default='Hyderabad, India')
    bio = models.TextField()
    hero_intro = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True)
    default_theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='dark')
    is_available = models.BooleanField(default=True)
    availability_text = models.CharField(max_length=200, default='Open to opportunities')
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.name

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_active=True).first()


class AboutStat(TimeStampedModel):
    label = models.CharField(max_length=100)
    value = models.PositiveIntegerField()
    suffix = models.CharField(max_length=10, blank=True, default='+')
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.label}: {self.value}{self.suffix}'


class TechBadge(TimeStampedModel):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class ArchitectureDiagram(TimeStampedModel):
    DIAGRAM_TYPES = [
        ('backend', 'Backend Architecture'),
        ('api_flow', 'API Flow'),
        ('microservices', 'Microservices Flow'),
        ('ai_pipeline', 'AI Workflow Pipeline'),
        ('deployment', 'Deployment Architecture'),
    ]

    title = models.CharField(max_length=200)
    diagram_type = models.CharField(max_length=20, choices=DIAGRAM_TYPES)
    description = models.TextField()
    svg_content = models.TextField(help_text='Inline SVG markup')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
