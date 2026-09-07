/* =====================================================
   querorango.com — main.js
   Shared JS: dark mode, PWA install, nav, toast, scroll
   ===================================================== */

(function () {
  'use strict';

  // ── Dark Mode ─────────────────────────────────────
  const THEME_KEY = 'qr-theme';
  const themeToggle = document.getElementById('theme-toggle');
  const html = document.documentElement;

  function applyTheme(theme) {
    html.setAttribute('data-theme', theme);
    localStorage.setItem(THEME_KEY, theme);
    if (themeToggle) {
      themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Modo claro' : 'Modo escuro');
      themeToggle.innerHTML = theme === 'dark' ? '☀️' : '🌙';
    }
  }

  function initTheme() {
    const saved = localStorage.getItem(THEME_KEY);
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(saved || (prefersDark ? 'dark' : 'light'));
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = html.getAttribute('data-theme');
      applyTheme(current === 'dark' ? 'light' : 'dark');
    });
  }

  initTheme();

  // ── Header scroll effect ───────────────────────────
  const header = document.querySelector('.site-header');
  window.addEventListener('scroll', () => {
    if (header) header.classList.toggle('scrolled', window.scrollY > 20);
  }, { passive: true });

  // ── Scroll progress bar ────────────────────────────
  const progressBar = document.querySelector('.scroll-progress');
  if (progressBar) {
    window.addEventListener('scroll', () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const pct = max > 0 ? (window.scrollY / max) * 100 : 0;
      progressBar.style.width = pct + '%';
    }, { passive: true });
  }

  // ── Mobile nav ─────────────────────────────────────
  const hamburger = document.querySelector('.nav-hamburger');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', isOpen);
      hamburger.innerHTML = isOpen ? '✕' : '☰';
      document.body.style.overflow = isOpen ? 'hidden' : '';
    });
    // Close on link click
    mobileMenu.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        hamburger.innerHTML = '☰';
        document.body.style.overflow = '';
      });
    });
  }

  // Mark active nav link
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link, .mobile-menu .nav-link').forEach(link => {
    const href = link.getAttribute('href');
    if (href && currentPath.startsWith(href) && href !== '/') {
      link.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      link.classList.add('active');
    }
  });

  // ── Nav Dropdown toggle (touch / click) ────────────
  const dropdowns = document.querySelectorAll('.nav-dropdown');
  dropdowns.forEach(drop => {
    const btn = drop.querySelector('.nav-dropdown-btn');
    if (btn) {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        drop.classList.toggle('active');
      });
    }
  });
  document.addEventListener('click', (e) => {
    dropdowns.forEach(drop => {
      if (!drop.contains(e.target)) {
        drop.classList.remove('active');
      }
    });
  });

  // ── TOC active state on scroll ─────────────────────
  const tocLinks = document.querySelectorAll('.toc a[href^="#"]');
  if (tocLinks.length) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          tocLinks.forEach(l => l.classList.remove('active'));
          const id = entry.target.getAttribute('id');
          const active = document.querySelector(`.toc a[href="#${id}"]`);
          if (active) active.classList.add('active');
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    tocLinks.forEach(l => {
      const target = document.querySelector(l.getAttribute('href'));
      if (target) observer.observe(target);
    });
  }

  // ── Toast notification ─────────────────────────────
  window.showToast = function (msg, type = '') {
    let toast = document.getElementById('qr-toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'qr-toast';
      toast.className = 'toast';
      document.body.appendChild(toast);
    }
    toast.textContent = msg;
    toast.className = 'toast' + (type ? ' ' + type : '');
    toast.classList.add('show');
    clearTimeout(toast._timeout);
    toast._timeout = setTimeout(() => toast.classList.remove('show'), 3000);
  };

  // ── Favorites (localStorage) ───────────────────────
  const FAV_KEY = 'qr-favorites';

  window.getFavorites = () => JSON.parse(localStorage.getItem(FAV_KEY) || '[]');

  window.toggleFavorite = function (id, title, url, img) {
    const favs = window.getFavorites();
    const idx = favs.findIndex(f => f.id === id);
    if (idx > -1) {
      favs.splice(idx, 1);
      showToast('❌ Removido dos favoritos');
    } else {
      favs.push({ id, title, url, img, addedAt: new Date().toISOString() });
      showToast('❤️ Salvo nos favoritos!', 'success');
    }
    localStorage.setItem(FAV_KEY, JSON.stringify(favs));
    updateFavBtn(id);
    return idx === -1;
  };

  window.updateFavBtn = function (id) {
    const btn = document.getElementById('fav-btn');
    if (!btn) return;
    const favs = window.getFavorites();
    const isFav = favs.some(f => f.id === id);
    btn.innerHTML = isFav ? '❤️ Salvo' : '🤍 Salvar';
    btn.setAttribute('aria-pressed', isFav);
  };

  // ── Share functionality ────────────────────────────
  window.shareRecipe = function (title, url) {
    if (navigator.share) {
      navigator.share({ title, url }).catch(() => {});
    } else {
      copyToClipboard(url);
    }
  };

  window.copyToClipboard = function (text) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(() => showToast('🔗 Link copiado!', 'success'));
    } else {
      const el = document.createElement('textarea');
      el.value = text;
      document.body.appendChild(el);
      el.select();
      document.execCommand('copy');
      document.body.removeChild(el);
      showToast('🔗 Link copiado!', 'success');
    }
  };

  // ── PWA Install Prompt ─────────────────────────────
  let deferredPrompt = null;
  const banner = document.getElementById('pwa-banner');
  const pwaBannerInstall = document.getElementById('pwa-install-btn');
  const pwaBannerClose = document.getElementById('pwa-banner-close');

  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault();
    deferredPrompt = e;
    if (banner && !localStorage.getItem('qr-pwa-dismissed')) {
      setTimeout(() => banner.classList.add('show'), 3000);
    }
  });

  if (pwaBannerInstall) {
    pwaBannerInstall.addEventListener('click', async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        const { outcome } = await deferredPrompt.userChoice;
        if (outcome === 'accepted') showToast('🎉 App instalado com sucesso!', 'success');
        deferredPrompt = null;
        banner?.classList.remove('show');
      }
    });
  }

  if (pwaBannerClose) {
    pwaBannerClose.addEventListener('click', () => {
      banner?.classList.remove('show');
      localStorage.setItem('qr-pwa-dismissed', '1');
    });
  }

  // ── Service Worker registration ────────────────────
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js')
        .catch(err => console.warn('SW registration failed:', err));
    });
  }

  // ── Intersection Observer for animations ───────────
  const animItems = document.querySelectorAll('[data-animate]');
  if (animItems.length) {
    const animObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
          animObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    animItems.forEach(el => animObserver.observe(el));
  }

  // ── Print recipe ───────────────────────────────────
  window.printRecipe = () => window.print();

  // ── Working LGPD Cookie Consent Banner ─────────────
  const COOKIE_CONSENT_KEY = 'qr-cookie-consent';

  function createCookieBanner() {
    if (document.getElementById('cookie-consent-banner')) return;

    const banner = document.createElement('div');
    banner.id = 'cookie-consent-banner';
    banner.className = 'cookie-banner';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'Consentimento de Cookies e Privacidade');

    banner.innerHTML = `
      <div>
        <div class="cookie-title">Sua Privacidade & Cookies 🍪</div>
        <p class="cookie-text">
          Utilizamos cookies essenciais para salvar suas receitas favoritas e checklists no seu aparelho, além de cookies para métricas de navegação. Você pode escolher suas preferências conforme nossa <a href="/politica-de-privacidade/" style="text-decoration: underline; font-weight: 600;">Política de Privacidade (LGPD)</a>.
        </p>
      </div>
      <div class="cookie-actions">
        <button id="cookie-accept-all" class="btn btn-primary btn-sm">Aceitar Todos</button>
        <button id="cookie-accept-essential" class="btn btn-ghost btn-sm">Apenas Necessários</button>
        <a href="/politica-de-privacidade/" class="btn-sm text-muted" style="text-decoration: underline; font-size: 0.8rem;">Saiba mais</a>
      </div>
    `;

    document.body.appendChild(banner);

    // Eventos dos botões
    document.getElementById('cookie-accept-all')?.addEventListener('click', () => {
      setCookieConsent('all');
    });

    document.getElementById('cookie-accept-essential')?.addEventListener('click', () => {
      setCookieConsent('essential');
    });

    // Mostrar com delay sutil
    setTimeout(() => {
      banner.classList.add('show');
    }, 800);
  }

  function setCookieConsent(type) {
    localStorage.setItem(COOKIE_CONSENT_KEY, JSON.stringify({
      consent: type,
      date: new Date().toISOString()
    }));
    const banner = document.getElementById('cookie-consent-banner');
    if (banner) {
      banner.classList.remove('show');
      setTimeout(() => banner.remove(), 400);
    }
    const msg = type === 'all' ? 'Preferências salvas: Todos os cookies aceitos.' : 'Preferências salvas: Apenas cookies essenciais.';
    showToast(msg, 'success');
  }

  // Inicializar se o usuário ainda não escolheu
  window.initCookieConsent = function () {
    const saved = localStorage.getItem(COOKIE_CONSENT_KEY);
    if (!saved) {
      createCookieBanner();
    }
  };

  // Permitir que o usuário altere a escolha a qualquer momento (ex: no rodapé)
  window.openCookiePreferences = function () {
    const existing = document.getElementById('cookie-consent-banner');
    if (existing) existing.remove();
    createCookieBanner();
  };

  // ── Functional Push Notifications System ──────────
  const NOTIF_STORAGE_KEY = 'qr-notifications-enabled';

  window.sendLocalNotification = function (title, body, url = '/') {
    if (!('Notification' in window) || Notification.permission !== 'granted') return;

    if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
      navigator.serviceWorker.ready.then(reg => {
        reg.showNotification(title, {
          body: body,
          icon: '/assets/icons/icon.svg',
          badge: '/assets/icons/icon.svg',
          vibrate: [200, 100, 200],
          tag: 'querorango-alert',
          data: { url: url }
        });
      });
    } else {
      try {
        new Notification(title, {
          body: body,
          icon: '/assets/icons/icon.svg'
        });
      } catch (e) {
        console.warn('Native notification fallback error:', e);
      }
    }
  };

  window.toggleNotifications = async function () {
    if (!('Notification' in window)) {
      showToast('⚠️ Seu navegador não suporta notificações.');
      return;
    }

    if (Notification.permission === 'granted') {
      // Já está ativado: avisa e dispara uma notificação de teste/exemplo
      showToast('🔔 Notificações já estão ativas!', 'success');
      window.sendLocalNotification(
        'Quero Rango 🍊',
        'Seu aviso de receitas está funcionando perfeitamente! Fique de olho nos próximos rangos.',
        '/receitas/'
      );
      updateNotifButtons(true);
      return;
    }

    if (Notification.permission === 'denied') {
      showToast('⚠️ As notificações estão bloqueadas nas configurações do seu navegador.');
      return;
    }

    // Solicitar permissão nativa
    try {
      const permission = await Notification.requestPermission();
      if (permission === 'granted') {
        localStorage.setItem(NOTIF_STORAGE_KEY, 'true');
        showToast('🎉 Notificações ativadas com sucesso!', 'success');
        updateNotifButtons(true);

        // Enviar notificação de boas-vindas imediata
        setTimeout(() => {
          window.sendLocalNotification(
            'Quero Rango 🍊 — Bem-vindo!',
            'Agora você receberá avisos das melhores receitas para não faltar ideia no seu almoço e sobremesa.',
            '/receitas/'
          );
        }, 600);

        // Ocultar banner de convite se houver
        const promptEl = document.getElementById('notif-prompt-banner');
        if (promptEl) promptEl.remove();
      } else {
        showToast('Notificações não foram ativadas.');
        updateNotifButtons(false);
      }
    } catch (err) {
      console.error('Erro ao pedir permissão de notificação:', err);
    }
  };

  function updateNotifButtons(isActive) {
    document.querySelectorAll('.notif-toggle-btn').forEach(btn => {
      if (isActive) {
        btn.classList.add('active');
        btn.setAttribute('title', 'Notificações Ativadas');
        btn.setAttribute('aria-label', 'Notificações Ativadas');
        btn.innerHTML = '🔔';
        btn.style.color = 'var(--primary)';
      } else {
        btn.classList.remove('active');
        btn.setAttribute('title', 'Ativar Notificações');
        btn.setAttribute('aria-label', 'Ativar Notificações');
        btn.innerHTML = '🔕';
        btn.style.color = '';
      }
    });
  }

  // Banner sutil de convite para ativar notificações após navegação
  function initNotificationPrompt() {
    if (!('Notification' in window)) return;
    if (Notification.permission === 'granted' || Notification.permission === 'denied') return;
    if (localStorage.getItem('qr-notif-prompt-dismissed')) return;

    setTimeout(() => {
      if (document.getElementById('notif-prompt-banner')) return;

      const prompt = document.createElement('div');
      prompt.id = 'notif-prompt-banner';
      prompt.className = 'notif-prompt';
      prompt.innerHTML = `
        <div style="font-size: 1.5rem; flex-shrink: 0;">🔔</div>
        <div style="flex: 1;">
          <strong style="font-size: 0.95rem; display: block; color: var(--text);">Receber receitas quentinhas?</strong>
          <small class="text-muted">Seja avisado quando sair uma nova receita ou dica culinária.</small>
        </div>
        <div style="display: flex; gap: 0.5rem; align-items: center;">
          <button id="notif-prompt-accept" class="btn btn-primary btn-sm">Ativar</button>
          <button id="notif-prompt-close" class="btn btn-ghost btn-sm" style="font-size: 0.75rem;">Depois</button>
        </div>
      `;

      document.body.appendChild(prompt);

      document.getElementById('notif-prompt-accept')?.addEventListener('click', () => {
        window.toggleNotifications();
        prompt.remove();
      });

      document.getElementById('notif-prompt-close')?.addEventListener('click', () => {
        localStorage.setItem('qr-notif-prompt-dismissed', '1');
        prompt.remove();
      });

      setTimeout(() => prompt.classList.add('show'), 100);
    }, 4500);
  }

  window.addEventListener('DOMContentLoaded', () => {
    window.initCookieConsent();
    if ('Notification' in window) {
      updateNotifButtons(Notification.permission === 'granted');
      initNotificationPrompt();
    }
  });

})();
