from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from apps.blog.models import BlogPost, Category, Tag
from apps.core.models import AboutStat, ArchitectureDiagram, SiteSettings, TechBadge
from apps.portfolio.models import Certification, Education, Experience, Project, Skill, SkillCategory

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed portfolio database with Shiva Shankar Chanda content'

    def handle(self, *args, **options):
        self.stdout.write('Seeding portfolio data...')

        SiteSettings.objects.all().delete()
        SiteSettings.objects.create(
            name='Shiva Shankar Chanda',
            title='Full Stack Software Engineer',
            location='Hyderabad, India',
            bio=(
                'Full Stack Software Engineer specializing in scalable backend systems, '
                'AI-powered applications, secure REST APIs, real-time platforms, and '
                'cloud-native deployments.'
            ),
            hero_intro=(
                'Full Stack Software Engineer with experience building scalable backend systems, '
                'AI-powered applications, REST APIs, real-time platforms, and cloud-native solutions '
                'using Django, FastAPI, React, PostgreSQL, Redis, Docker, and AWS.'
            ),
            email='shivashankar@example.com',
            default_theme='dark',
            is_available=True,
            availability_text='Open to opportunities',
            meta_description='Shiva Shankar Chanda — Full Stack & Backend Engineer | Django, FastAPI, AI',
            meta_keywords='Django, FastAPI, Backend, AI, PostgreSQL, AWS, Full Stack',
        )

        AboutStat.objects.all().delete()
        stats = [
            ('Years Experience', 3, '+', 'briefcase'),
            ('Projects Built', 15, '+', 'folder-open'),
            ('Technologies', 50, '+', 'code'),
            ('AI Integrations', 5, '+', 'brain'),
        ]
        for i, (label, val, suffix, icon) in enumerate(stats):
            AboutStat.objects.create(label=label, value=val, suffix=suffix, icon=icon, order=i)

        TechBadge.objects.all().delete()
        for i, name in enumerate(['Python', 'Django', 'DRF', 'FastAPI', 'PostgreSQL', 'React', 'Redis', 'Docker', 'AWS', 'Kubernetes']):
            TechBadge.objects.create(name=name, order=i)

        self._seed_skills()
        self._seed_experience()
        self._seed_projects()
        self._seed_certifications()
        self._seed_education()
        self._seed_architecture()
        self._seed_blog()

        self.stdout.write(self.style.SUCCESS('Portfolio seeded successfully!'))

    def _seed_skills(self):
        SkillCategory.objects.all().delete()
        categories = {
            'Backend': {
                'icon': 'server',
                'skills': [
                    ('Python', 95), ('Django', 92), ('Django REST Framework', 90),
                    ('FastAPI', 88), ('Flask', 75), ('REST APIs', 93),
                    ('WebSockets', 85), ('Celery', 82), ('Redis', 88),
                    ('GraphQL', 70), ('gRPC', 72),
                ],
            },
            'Frontend': {
                'icon': 'display',
                'skills': [
                    ('React.js', 85), ('Next.js', 80), ('HTML5', 95), ('CSS3', 92),
                    ('JavaScript', 90), ('TypeScript', 82), ('Redux', 78), ('Responsive UI', 90),
                ],
            },
            'Databases': {
                'icon': 'database',
                'skills': [
                    ('PostgreSQL', 92), ('MySQL', 85), ('Redis', 88), ('MongoDB', 75),
                    ('Elasticsearch', 70), ('DynamoDB', 68), ('Pinecone', 72),
                ],
            },
            'AI / ML': {
                'icon': 'brain',
                'skills': [
                    ('RAG', 85), ('OpenCV', 78), ('TensorFlow', 75), ('PyTorch', 72),
                    ('Embeddings', 88), ('Semantic Search', 85), ('LangChain', 82),
                    ('LLM Integrations', 86), ('AI Automation', 84),
                ],
            },
            'Cloud & DevOps': {
                'icon': 'cloud',
                'skills': [
                    ('AWS', 88), ('Docker', 90), ('Kubernetes', 75), ('CI/CD', 85),
                    ('Terraform', 70), ('NGINX', 82), ('Linux', 88), ('Azure', 72), ('Google Cloud', 70),
                ],
            },
            'Security & Architecture': {
                'icon': 'shield-halved',
                'skills': [
                    ('JWT', 92), ('OAuth', 85), ('RBAC', 88), ('SSL/TLS', 85),
                    ('OWASP', 80), ('SOLID Principles', 90), ('Clean Architecture', 88), ('System Design', 85),
                ],
            },
        }
        for order, (cat_name, data) in enumerate(categories.items()):
            cat = SkillCategory.objects.create(
                name=cat_name, slug=slugify(cat_name), icon=data['icon'], order=order
            )
            for i, (skill_name, prof) in enumerate(data['skills']):
                Skill.objects.create(category=cat, name=skill_name, proficiency=prof, order=i)

    def _seed_experience(self):
        Experience.objects.all().delete()
        experiences = [
            {
                'company': 'Avsys International India Pvt Ltd',
                'role': 'Full Stack Developer',
                'start_date': 'Aug 2024',
                'end_date': 'Present',
                'responsibilities': [
                    'Developed scalable backend microservices using Django, DRF, FastAPI',
                    'Built secure REST APIs',
                    'Implemented WebSockets for real-time systems',
                    'Worked with PostgreSQL/MySQL optimization',
                    'JWT authentication and RBAC',
                    'AI workflow integrations',
                    'AWS deployment and Docker containerization',
                    'CI/CD and monitoring',
                ],
                'technologies': 'Django, DRF, FastAPI, PostgreSQL, AWS, Docker',
            },
            {
                'company': 'Bharath Intern',
                'role': 'Full Stack Developer Intern',
                'start_date': 'Jan 2024',
                'end_date': 'May 2024',
                'responsibilities': [
                    'Media streaming platform development',
                    'React frontend implementation',
                    'API integrations',
                    'Recommendation logic',
                    'Azure deployment',
                    'Performance optimization',
                ],
                'technologies': 'React, Node.js, Azure',
            },
            {
                'company': 'Interpe',
                'role': 'Full Stack Developer Intern',
                'start_date': 'Jul 2023',
                'end_date': 'Nov 2023',
                'responsibilities': [
                    'E-commerce platform development',
                    'Django backend',
                    'Authentication systems',
                    'AWS deployment',
                    'Secure application development',
                ],
                'technologies': 'Django, AWS, PostgreSQL',
            },
        ]
        for i, exp in enumerate(experiences):
            Experience.objects.create(order=i, **exp)

    def _seed_projects(self):
        Project.objects.all().delete()
        projects = [
            {
                'title': 'AI-Powered FinTech Risk & Fraud Intelligence Platform',
                'slug': 'fintech-fraud-intelligence',
                'short_description': 'AI-powered fraud detection and financial intelligence platform.',
                'description': (
                    'An AI-powered fraud detection and financial intelligence platform using FastAPI, '
                    'React.js, PostgreSQL, Redis, embeddings, OCR, RAG, semantic search, and ML-based anomaly detection.'
                ),
                'features': [
                    'Fraud detection engine', 'AI document intelligence', 'KYC processing',
                    'JWT + RBAC security', 'Redis caching', 'Docker deployment', 'CI/CD pipelines',
                ],
                'tech_stack': 'Python, FastAPI, React.js, PostgreSQL, Redis, Docker, AWS',
                'is_featured': True,
            },
            {
                'title': 'Real-Time Simulation Platform',
                'slug': 'realtime-simulation',
                'short_description': 'WebSocket-based real-time simulation with Django backend.',
                'description': 'Scalable real-time simulation platform with WebSocket communication and Redis pub/sub.',
                'features': ['WebSockets', 'Real-time updates', 'Django Channels', 'Redis'],
                'tech_stack': 'Python, Django, WebSockets, Redis, PostgreSQL',
                'is_featured': True,
            },
            {
                'title': 'AI Computer Vision Monitoring System',
                'slug': 'cv-monitoring',
                'short_description': 'Computer vision monitoring with OpenCV and ML pipelines.',
                'description': 'AI-powered computer vision system for real-time monitoring and anomaly detection.',
                'features': ['OpenCV', 'TensorFlow', 'Real-time inference', 'Alert system'],
                'tech_stack': 'Python, OpenCV, TensorFlow, FastAPI, Docker',
                'is_featured': True,
            },
            {
                'title': 'Media Streaming Web App',
                'slug': 'media-streaming',
                'short_description': 'Full-stack media streaming platform with React frontend.',
                'description': 'Media streaming web application with recommendation engine and Azure deployment.',
                'features': ['Streaming', 'Recommendations', 'React UI', 'Azure CDN'],
                'tech_stack': 'React, Node.js, Azure, PostgreSQL',
                'is_featured': False,
            },
            {
                'title': 'E-Commerce Platform',
                'slug': 'ecommerce-platform',
                'short_description': 'Secure e-commerce platform with Django backend.',
                'description': 'Full-featured e-commerce platform with authentication, payments, and AWS deployment.',
                'features': ['Django backend', 'Auth systems', 'AWS deployment', 'Secure checkout'],
                'tech_stack': 'Django, PostgreSQL, AWS, React',
                'is_featured': False,
            },
        ]
        for i, p in enumerate(projects):
            Project.objects.create(order=i, is_active=True, github_url='#', live_url='#', **p)

    def _seed_certifications(self):
        Certification.objects.all().delete()
        certs = [
            'Data Structures and Algorithms in Python',
            'Kimo Python Certificate',
            'ReactJS Workshop',
        ]
        for i, title in enumerate(certs):
            Certification.objects.create(title=title, order=i)

    def _seed_education(self):
        Education.objects.all().delete()
        Education.objects.create(
            institution='TKR College of Engineering and Technology',
            degree='Bachelor of Technology',
            field_of_study='Computer Science and Engineering',
            cgpa=8.30,
            coursework=[
                'Data Structures', 'Operating Systems', 'DBMS',
                'Cloud Computing', 'Machine Learning', 'Distributed Systems',
            ],
        )

    def _seed_architecture(self):
        ArchitectureDiagram.objects.all().delete()

    def _seed_blog(self):
        user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@portfolio.local', 'is_staff': True, 'is_superuser': True},
        )
        if not user.has_usable_password():
            user.set_password('admin123')
            user.save()

        categories = ['Django', 'FastAPI', 'AI Engineering', 'System Design', 'DevOps', 'Cloud', 'APIs']
        for name in categories:
            Category.objects.get_or_create(name=name, defaults={'slug': slugify(name)})

        tag, _ = Tag.objects.get_or_create(name='Backend', defaults={'slug': 'backend'})
        django_cat = Category.objects.get(slug='django')

        if not BlogPost.objects.filter(slug='building-scalable-django-apis').exists():
            BlogPost.objects.create(
                title='Building Scalable Django REST APIs',
                slug='building-scalable-django-apis',
                author=user,
                excerpt='Best practices for designing production-ready Django REST Framework APIs.',
                content='## Introduction\n\nBuilding scalable APIs requires clean architecture, proper serialization, and caching strategies.\n\n## Service Layer\n\nSeparate business logic from views using a dedicated service layer.\n\n## Caching\n\nUse Redis for response caching and session management.',
                category=django_cat,
                status='published',
                is_featured=True,
                published_at=timezone.now(),
            ).tags.add(tag)
