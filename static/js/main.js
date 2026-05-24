/**
 * Shiva Shankar Chanda Portfolio — Main JavaScript
 */
(function () {
  'use strict';

  const API_BASE = '/api/v1';
  const TYPING_PHRASES = [
    'Full Stack Developer',
    'Backend Engineer',
    'AI Integration Developer',
    'Django & FastAPI Specialist',
  ];

  // --- Loader ---
  window.addEventListener('load', () => {
    setTimeout(() => document.getElementById('loader')?.classList.add('hidden'), 800);
  });

  // --- Theme ---
  const themeToggle = document.getElementById('themeToggle');
  const html = document.documentElement;
  const savedTheme = localStorage.getItem('theme') || 'dark';
  html.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  themeToggle?.addEventListener('click', () => {
    const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateThemeIcon(next);
  });

  function updateThemeIcon(theme) {
    const icon = themeToggle?.querySelector('i');
    if (icon) icon.className = theme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
  }

  // --- Navbar ---
  const navbar = document.getElementById('navbar');
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');

  window.addEventListener('scroll', () => {
    navbar?.classList.toggle('scrolled', window.scrollY > 50);
    const progress = document.getElementById('scrollProgress');
    if (progress) {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = h > 0 ? `${(window.scrollY / h) * 100}%` : '0%';
    }
  });

  navToggle?.addEventListener('click', () => navLinks?.classList.toggle('open'));
  navLinks?.querySelectorAll('a').forEach((a) => {
    a.addEventListener('click', () => navLinks.classList.remove('open'));
  });

  // --- Custom Cursor ---
  const dot = document.getElementById('cursorDot');
  const outline = document.getElementById('cursorOutline');
  if (dot && outline && window.matchMedia('(min-width: 769px)').matches) {
    document.addEventListener('mousemove', (e) => {
      dot.style.left = `${e.clientX}px`;
      dot.style.top = `${e.clientY}px`;
      outline.style.left = `${e.clientX}px`;
      outline.style.top = `${e.clientY}px`;
    });
    document.querySelectorAll('a, button, .glass-card').forEach((el) => {
      el.addEventListener('mouseenter', () => {
        outline.style.width = '56px';
        outline.style.height = '56px';
      });
      el.addEventListener('mouseleave', () => {
        outline.style.width = '36px';
        outline.style.height = '36px';
      });
    });
  }

  // --- Typing Effect ---
  const typingEl = document.getElementById('typingText');
  if (typingEl) {
    let phraseIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    function type() {
      const current = TYPING_PHRASES[phraseIndex];
      typingEl.textContent = isDeleting
        ? current.substring(0, charIndex - 1)
        : current.substring(0, charIndex + 1);
      charIndex = isDeleting ? charIndex - 1 : charIndex + 1;

      let delay = isDeleting ? 50 : 100;
      if (!isDeleting && charIndex === current.length) {
        delay = 2000;
        isDeleting = true;
      } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        phraseIndex = (phraseIndex + 1) % TYPING_PHRASES.length;
        delay = 500;
      }
      setTimeout(type, delay);
    }
    type();
  }

  // --- Particle Background ---
  const canvas = document.getElementById('particles-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let particles = [];
    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    resize();
    window.addEventListener('resize', resize);

    for (let i = 0; i < 80; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 2 + 0.5,
        dx: (Math.random() - 0.5) * 0.5,
        dy: (Math.random() - 0.5) * 0.5,
      });
    }

    function animateParticles() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const color = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || '#6366f1';
      particles.forEach((p, i) => {
        p.x += p.dx;
        p.y += p.dy;
        if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
        if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.globalAlpha = 0.5;
        ctx.fill();
        particles.slice(i + 1).forEach((p2) => {
          const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
          if (dist < 120) {
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.strokeStyle = color;
            ctx.globalAlpha = 0.1;
            ctx.stroke();
          }
        });
      });
      ctx.globalAlpha = 1;
      requestAnimationFrame(animateParticles);
    }
    animateParticles();
  }

  // --- Stat Counters ---
  const statObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        const card = entry.target;
        const target = parseInt(card.dataset.count, 10);
        const numEl = card.querySelector('.stat-number');
        let current = 0;
        const step = Math.ceil(target / 60);
        const timer = setInterval(() => {
          current += step;
          if (current >= target) {
            current = target;
            clearInterval(timer);
          }
          if (numEl) numEl.textContent = current;
        }, 30);
        statObserver.unobserve(card);
      });
    },
    { threshold: 0.5 }
  );
  document.querySelectorAll('.stat-card').forEach((c) => statObserver.observe(c));

  // --- Skill Progress Bars ---
  const skillObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.style.width = `${entry.target.dataset.progress}%`;
        skillObserver.unobserve(entry.target);
      });
    },
    { threshold: 0.3 }
  );
  document.querySelectorAll('.skill-progress').forEach((bar) => skillObserver.observe(bar));

  // --- Timeline ---
  const timelineObserver = new IntersectionObserver(
    (entries) => entries.forEach((e) => e.isIntersecting && e.target.classList.add('visible')),
    { threshold: 0.2 }
  );
  document.querySelectorAll('.timeline-item').forEach((item) => timelineObserver.observe(item));

  // --- Contact Form ---
  const contactForm = document.getElementById('contactForm');
  contactForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const status = document.getElementById('formStatus');
    const data = {
      name: contactForm.name.value,
      email: contactForm.email.value,
      subject: contactForm.subject.value,
      message: contactForm.message.value,
    };
    try {
      const res = await fetch(`${API_BASE}/contact/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrf() },
        body: JSON.stringify(data),
      });
      if (res.ok) {
        status.textContent = 'Message sent successfully!';
        status.className = 'form-status success';
        contactForm.reset();
      } else {
        throw new Error('Failed');
      }
    } catch {
      status.textContent = 'Failed to send. Please try again.';
      status.className = 'form-status error';
    }
  });

  // --- Resume Analyzer ---
  document.getElementById('analyzeResume')?.addEventListener('click', async () => {
    const text = document.getElementById('resumeText')?.value;
    if (!text?.trim()) return;
    const res = await fetch(`${API_BASE}/resume/analyze/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    const results = document.getElementById('analyzerResults');
    results.hidden = false;
    document.getElementById('analyzerScore').textContent = data.score;
    document.getElementById('analyzerSummary').textContent = data.summary;
    document.getElementById('analyzerKeywords').innerHTML =
      data.matched_keywords?.map((k) => `<span class="tech-tag">${k}</span>`).join('') || '';
    document.getElementById('analyzerSuggestions').innerHTML =
      data.suggestions?.map((s) => `<li>${s}</li>`).join('') || '';
  });

  // --- Chatbot ---
  let chatSessionId = localStorage.getItem('chatSession') || crypto.randomUUID?.() || Date.now().toString();
  localStorage.setItem('chatSession', chatSessionId);

  const chatToggle = document.getElementById('chatbotToggle');
  const chatPanel = document.getElementById('chatbotPanel');
  const chatClose = document.getElementById('chatbotClose');
  const chatForm = document.getElementById('chatbotForm');
  const chatMessages = document.getElementById('chatbotMessages');

  chatToggle?.addEventListener('click', () => chatPanel?.classList.toggle('open'));
  chatClose?.addEventListener('click', () => chatPanel?.classList.remove('open'));

  chatForm?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const input = chatForm.querySelector('input');
    const msg = input.value.trim();
    if (!msg) return;
    appendChat('user', msg);
    input.value = '';
    try {
      const res = await fetch(`${API_BASE}/chatbot/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg, session_id: chatSessionId }),
      });
      const data = await res.json();
      chatSessionId = data.session_id;
      appendChat('assistant', data.response);
    } catch {
      appendChat('assistant', 'Sorry, I am temporarily unavailable.');
    }
  });

  function appendChat(role, text) {
    const div = document.createElement('div');
    div.className = `chat-msg ${role}`;
    div.textContent = text;
    chatMessages?.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  // --- Blog Comment ---
  document.getElementById('commentForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;
    const slug = form.dataset.slug;
    const body = {
      author_name: form.author_name.value,
      author_email: form.author_email.value,
      content: form.content.value,
    };
    await fetch(`${API_BASE}/blog/${slug}/comment/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    alert('Comment submitted for approval.');
    form.reset();
  });

  // --- PWA Service Worker ---
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  }

  function getCsrf() {
    const cookie = document.cookie.split(';').find((c) => c.trim().startsWith('csrftoken='));
    return cookie ? cookie.split('=')[1] : '';
  }
})();
