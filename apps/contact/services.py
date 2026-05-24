from django.conf import settings
from django.core.mail import send_mail

from .models import ChatMessage, ContactMessage


class ContactService:
    @staticmethod
    def create_message(data: dict, request=None) -> ContactMessage:
        ip = None
        ua = ''
        if request:
            ip = request.META.get('REMOTE_ADDR')
            ua = request.META.get('HTTP_USER_AGENT', '')[:500]

        message = ContactMessage.objects.create(
            name=data['name'],
            email=data['email'],
            subject=data['subject'],
            message=data['message'],
            ip_address=ip,
            user_agent=ua,
        )
        ContactService.send_notification(message)
        return message

    @staticmethod
    def send_notification(message: ContactMessage):
        recipient = settings.CONTACT_NOTIFICATION_EMAIL or settings.DEFAULT_FROM_EMAIL
        if not recipient:
            return
        subject = f'[Portfolio Contact] {message.subject}'
        body = (
            f'Name: {message.name}\n'
            f'Email: {message.email}\n'
            f'Subject: {message.subject}\n\n'
            f'{message.message}'
        )
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient], fail_silently=True)

    @staticmethod
    def mark_as_read(message: ContactMessage):
        message.status = 'read'
        message.save(update_fields=['status', 'updated_at'])


class ChatbotService:
    RESPONSES = {
        'skills': 'I specialize in Django, FastAPI, DRF, PostgreSQL, Redis, React, AWS, Docker, and AI integrations including RAG and LLM workflows.',
        'experience': 'I am a Full Stack Developer at Avsys International (Aug 2024–Present), with prior internships at Bharath Intern and Interpe.',
        'projects': 'Featured projects include an AI-Powered FinTech Fraud Platform, Real-Time Simulation, Computer Vision Monitoring, Media Streaming, and E-Commerce platforms.',
        'contact': 'Use the contact form on this site or reach out via LinkedIn/GitHub links in the hero section.',
        'resume': 'You can download my resume from the About section or hero CTA button.',
        'default': 'I am Shiva\'s AI portfolio assistant. Ask about skills, experience, projects, contact, or resume!',
    }

    KEYWORDS = {
        'skill': 'skills', 'django': 'skills', 'fastapi': 'skills', 'python': 'skills',
        'experience': 'experience', 'work': 'experience', 'job': 'experience', 'avsys': 'experience',
        'project': 'projects', 'portfolio': 'projects', 'fintech': 'projects',
        'contact': 'contact', 'email': 'contact', 'hire': 'contact',
        'resume': 'resume', 'cv': 'resume', 'download': 'resume',
    }

    @classmethod
    def get_response(cls, user_message: str, session_id: str) -> str:
        lower = user_message.lower()
        response_key = 'default'
        for keyword, key in cls.KEYWORDS.items():
            if keyword in lower:
                response_key = key
                break
        response = cls.RESPONSES[response_key]
        ChatMessage.objects.create(session_id=session_id, role='user', content=user_message)
        ChatMessage.objects.create(session_id=session_id, role='assistant', content=response)
        return response


class ResumeAnalyzerService:
    KEYWORD_SCORES = {
        'django': 10, 'fastapi': 10, 'python': 8, 'postgresql': 8, 'redis': 7,
        'docker': 7, 'aws': 7, 'react': 6, 'kubernetes': 6, 'rest': 5, 'api': 5,
        'machine learning': 8, 'ai': 7, 'rag': 8, 'tensorflow': 6, 'pytorch': 6,
        'celery': 5, 'graphql': 5, 'microservice': 7, 'ci/cd': 6,
    }

    @classmethod
    def analyze(cls, text: str) -> dict:
        lower = text.lower()
        matched = []
        score = 0
        for keyword, points in cls.KEYWORD_SCORES.items():
            if keyword in lower:
                matched.append(keyword)
                score += points
        max_score = sum(cls.KEYWORD_SCORES.values())
        percentage = min(100, int((score / max_score) * 100 * 3))
        suggestions = []
        for kw in ['django', 'fastapi', 'postgresql', 'docker', 'aws', 'rag']:
            if kw not in matched:
                suggestions.append(f'Consider highlighting {kw.upper()} experience')
        return {
            'score': percentage,
            'matched_keywords': matched,
            'suggestions': suggestions[:5],
            'summary': cls._get_summary(percentage),
        }

    @staticmethod
    def _get_summary(score: int) -> str:
        if score >= 80:
            return 'Excellent backend & AI alignment for senior engineering roles.'
        if score >= 50:
            return 'Good technical profile — strengthen cloud and AI keywords.'
        return 'Add more backend, cloud, and AI-specific technologies to improve match rate.'
