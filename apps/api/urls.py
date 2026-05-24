from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'blog', views.BlogPostViewSet, basename='blog')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'admin/projects', views.AdminProjectViewSet, basename='admin-project')
router.register(r'admin/comments', views.AdminCommentViewSet, basename='admin-comment')

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('site/', views.SiteSettingsView.as_view(), name='site-settings'),
    path('about/stats/', views.AboutStatListView.as_view(), name='about-stats'),
    path('about/badges/', views.TechBadgeListView.as_view(), name='tech-badges'),
    path('skills/', views.SkillCategoryListView.as_view(), name='skills'),
    path('experience/', views.ExperienceListView.as_view(), name='experience'),
    path('certifications/', views.CertificationListView.as_view(), name='certifications'),
    path('education/', views.EducationListView.as_view(), name='education'),
    path('architecture/', views.ArchitectureDiagramListView.as_view(), name='architecture'),
    path('contact/', views.ContactCreateView.as_view(), name='contact'),
    path('chatbot/', views.ChatbotView.as_view(), name='chatbot'),
    path('resume/analyze/', views.ResumeAnalyzerView.as_view(), name='resume-analyze'),
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin-dashboard'),
    path('', include(router.urls)),
]
