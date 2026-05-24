from typing import Optional

from .models import Project, SkillCategory


class ProjectService:
    @staticmethod
    def get_featured(limit: int = 6):
        return Project.objects.filter(is_featured=True, is_active=True)[:limit]

    @staticmethod
    def get_by_slug(slug: str) -> Optional[Project]:
        return Project.objects.filter(slug=slug, is_active=True).first()


class SkillService:
    @staticmethod
    def get_categorized():
        return SkillCategory.objects.prefetch_related('skills').all()
