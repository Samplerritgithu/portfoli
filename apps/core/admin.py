from django.contrib import admin

from .models import AboutStat, ArchitectureDiagram, SiteSettings, TechBadge


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'default_theme', 'is_available', 'is_active')
    list_editable = ('is_available', 'is_active', 'default_theme')


@admin.register(AboutStat)
class AboutStatAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'suffix', 'order')
    list_editable = ('order',)


@admin.register(TechBadge)
class TechBadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_featured')
    list_editable = ('order', 'is_featured')


@admin.register(ArchitectureDiagram)
class ArchitectureDiagramAdmin(admin.ModelAdmin):
    list_display = ('title', 'diagram_type', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('diagram_type',)
