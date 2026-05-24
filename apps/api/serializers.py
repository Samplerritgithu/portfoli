from rest_framework import serializers

from apps.blog.models import BlogPost, Category, Comment, Tag
from apps.contact.models import ContactMessage
from apps.core.models import AboutStat, ArchitectureDiagram, SiteSettings, TechBadge
from apps.portfolio.models import Certification, Education, Experience, Project, Skill, SkillCategory


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'


class AboutStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutStat
        fields = '__all__'


class TechBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechBadge
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'proficiency', 'icon', 'order']


class SkillCategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'slug', 'icon', 'order', 'skills']


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    tech_list = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_tech_list(self, obj):
        return obj.get_tech_list()


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class ArchitectureDiagramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArchitectureDiagram
        fields = '__all__'


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    def create(self, validated_data):
        from apps.contact.services import ContactService
        request = self.context.get('request')
        return ContactService.create_message(validated_data, request)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class BlogPostListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'category_name', 'status', 'is_featured', 'view_count', 'published_at',
        ]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'content', 'parent']

    def create(self, validated_data):
        from apps.blog.services import BlogService
        post = self.context['post']
        return BlogService.create_comment(post, validated_data)


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=2000)
    session_id = serializers.CharField(max_length=100, required=False)


class ResumeAnalyzeSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=50000)
