import uuid

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.blog.models import BlogPost, Category, Comment, Tag
from apps.blog.services import BlogService
from apps.contact.services import ChatbotService, ResumeAnalyzerService
from apps.core.models import AboutStat, ArchitectureDiagram, SiteSettings, TechBadge
from apps.portfolio.models import Certification, Education, Experience, Project, SkillCategory

from .permissions import IsAdminUserRole
from .serializers import (
    AboutStatSerializer,
    ArchitectureDiagramSerializer,
    BlogPostDetailSerializer,
    BlogPostListSerializer,
    CategorySerializer,
    CertificationSerializer,
    ChatRequestSerializer,
    CommentSerializer,
    ContactMessageSerializer,
    EducationSerializer,
    ExperienceSerializer,
    ProjectSerializer,
    ResumeAnalyzeSerializer,
    SiteSettingsSerializer,
    SkillCategorySerializer,
    TagSerializer,
    TechBadgeSerializer,
)


class SiteSettingsView(generics.RetrieveAPIView):
    serializer_class = SiteSettingsSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return SiteSettings.get_active()


class AboutStatListView(generics.ListAPIView):
    queryset = AboutStat.objects.all()
    serializer_class = AboutStatSerializer
    permission_classes = [AllowAny]


class TechBadgeListView(generics.ListAPIView):
    queryset = TechBadge.objects.filter(is_featured=True)
    serializer_class = TechBadgeSerializer
    permission_classes = [AllowAny]


class SkillCategoryListView(generics.ListAPIView):
    queryset = SkillCategory.objects.prefetch_related('skills')
    serializer_class = SkillCategorySerializer
    permission_classes = [AllowAny]


class ExperienceListView(generics.ListAPIView):
    queryset = Experience.objects.filter(is_active=True)
    serializer_class = ExperienceSerializer
    permission_classes = [AllowAny]


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(is_active=True)
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'tech_stack']
    ordering_fields = ['order', 'created_at']

    @action(detail=False, methods=['get'])
    def featured(self, request):
        qs = self.queryset.filter(is_featured=True)[:6]
        return Response(self.get_serializer(qs, many=True).data)


class CertificationListView(generics.ListAPIView):
    queryset = Certification.objects.filter(is_active=True)
    serializer_class = CertificationSerializer
    permission_classes = [AllowAny]


class EducationListView(generics.ListAPIView):
    queryset = Education.objects.filter(is_active=True)
    serializer_class = EducationSerializer
    permission_classes = [AllowAny]


class ArchitectureDiagramListView(generics.ListAPIView):
    queryset = ArchitectureDiagram.objects.filter(is_active=True)
    serializer_class = ArchitectureDiagramSerializer
    permission_classes = [AllowAny]


class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]


class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category__slug', 'tags__slug', 'is_featured']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['published_at', 'view_count']

    def get_queryset(self):
        return BlogService.get_published_posts()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        BlogService.increment_views(instance)
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['rendered_content'] = BlogService.render_content(instance)
        return Response(data)

    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def comment(self, request, slug=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data, context={'post': post})
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()
        return Response({'id': comment.id, 'message': 'Comment submitted for approval.'}, status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class ChatbotView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_id = serializer.validated_data.get('session_id') or str(uuid.uuid4())
        response = ChatbotService.get_response(serializer.validated_data['message'], session_id)
        return Response({'response': response, 'session_id': session_id})


class ResumeAnalyzerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResumeAnalyzeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = ResumeAnalyzerService.analyze(serializer.validated_data['text'])
        return Response(result)


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get(self, request):
        from apps.contact.models import ContactMessage
        return Response({
            'projects': Project.objects.count(),
            'blog_posts': BlogPost.objects.count(),
            'unread_messages': ContactMessage.objects.filter(status='new').count(),
            'skills': SkillCategory.objects.count(),
            'certifications': Certification.objects.count(),
        })


class AdminProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]
    lookup_field = 'slug'


class AdminCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAdminUserRole]

    def get_serializer_class(self):
        from rest_framework import serializers as drf_serializers
        class AdminCommentSerializer(drf_serializers.ModelSerializer):
            class Meta:
                model = Comment
                fields = '__all__'
        return AdminCommentSerializer
