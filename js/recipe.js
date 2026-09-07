/* =====================================================
   querorango.com — recipe.js
   Recipe page interactions:
   - Ingredient checklist
   - Step checklist + completion progress
   - Portions slider (auto-recalculate amounts)
   - Integrated timer
   - Modo Cozinhando (cooking mode)
   - FAQ accordion
   - Star rating
   ===================================================== */

(function () {
  'use strict';

  // ── Ingredient Checklist ───────────────────────────
  document.querySelectorAll('.ingredient-item').forEach(item => {
    item.addEventListener('click', () => {
      item.classList.toggle('checked');
      saveCheckState();
    });
  });

  // ── Step Checklist ─────────────────────────────────
  const steps = document.querySelectorAll('.step-item');
  const progressEl = document.getElementById('recipe-progress');
  const progressText = document.getElementById('recipe-progress-text');

  steps.forEach(step => {
    step.addEventListener('click', e => {
      // Don't toggle if clicking timer button
      if (e.target.closest('.step-timer-btn')) return;
      step.classList.toggle('checked');
      updateProgress();
      saveCheckState();
    });
  });

  function updateProgress() {
    const total = steps.length;
    const done = document.querySelectorAll('.step-item.checked').length;
    const pct = total ? Math.round((done / total) * 100) : 0;
    if (progressEl) progressEl.style.width = pct + '%';
    if (progressText) progressText.textContent = `${done} de ${total} passos concluídos`;
    if (pct === 100 && total > 0) {
      window.showToast && window.showToast('🎉 Receita concluída! Bom apetite!', 'success');
    }
  }

  // ── Persist checkbox state ─────────────────────────
  function saveCheckState() {
    const key = 'qr-check-' + window.location.pathname;
    const ingr = [...document.querySelectorAll('.ingredient-item')]
      .map(el => el.classList.contains('checked'));
    const stps = [...document.querySelectorAll('.step-item')]
      .map(el => el.classList.contains('checked'));
    localStorage.setItem(key, JSON.stringify({ ingr, stps }));
  }

  function loadCheckState() {
    const key = 'qr-check-' + window.location.pathname;
    try {
      const data = JSON.parse(localStorage.getItem(key));
      if (!data) return;
      const ingrItems = document.querySelectorAll('.ingredient-item');
      const stpItems = document.querySelectorAll('.step-item');
      data.ingr?.forEach((checked, i) => {
        if (checked && ingrItems[i]) ingrItems[i].classList.add('checked');
      });
      data.stps?.forEach((checked, i) => {
        if (checked && stpItems[i]) stpItems[i].classList.add('checked');
      });
      updateProgress();
    } catch (e) {}
  }

  loadCheckState();

  // ── Portions Slider ────────────────────────────────
  const slider = document.getElementById('portions-slider');
  const portionsValue = document.getElementById('portions-value');
  const BASE_PORTIONS = slider ? parseInt(slider.getAttribute('data-base'), 10) || 4 : 4;

  if (slider) {
    slider.addEventListener('input', () => {
      const newPortions = parseInt(slider.value, 10);
      if (portionsValue) {
        portionsValue.textContent = newPortions + ' ' + (newPortions === 1 ? 'porção' : 'porções');
      }
      recalculateIngredients(newPortions);
    });
  }

  function recalculateIngredients(newPortions) {
    document.querySelectorAll('[data-amount]').forEach(el => {
      const base = parseFloat(el.getAttribute('data-amount'));
      const unit = el.getAttribute('data-unit') || '';
      if (!isNaN(base)) {
        const newAmount = (base * newPortions / BASE_PORTIONS);
        const formatted = newAmount % 1 === 0 ? newAmount.toFixed(0)
          : newAmount < 0.25 ? '¼'
          : newAmount < 0.5 ? '½'
          : newAmount < 0.75 ? '¾'
          : newAmount.toFixed(1);
        el.textContent = formatted + (unit ? ' ' + unit : '');
      }
    });
  }

  // ── Reset checklist button ─────────────────────────
  const resetBtn = document.getElementById('reset-checks');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      document.querySelectorAll('.ingredient-item.checked, .step-item.checked')
        .forEach(el => el.classList.remove('checked'));
      updateProgress();
      const key = 'qr-check-' + window.location.pathname;
      localStorage.removeItem(key);
      window.showToast && window.showToast('♻️ Checklist reiniciado');
    });
  }

  // ── Integrated Timer ───────────────────────────────
  const timerModal = document.getElementById('timer-modal');
  const timerDisplay = document.getElementById('timer-display');
  const timerLabel = document.getElementById('timer-label');
  const timerStart = document.getElementById('timer-start');
  const timerPause = document.getElementById('timer-pause');
  const timerClose = document.getElementById('timer-close');

  let timerInterval = null;
  let timerSeconds = 0;
  let timerRunning = false;

  document.querySelectorAll('.step-timer-btn').forEach(btn => {
    btn.addEventListener('click', e => {
      e.stopPropagation();
      const mins = parseInt(btn.getAttribute('data-minutes'), 10) || 5;
      timerSeconds = mins * 60;
      if (timerLabel) timerLabel.textContent = btn.getAttribute('data-label') || `Timer de ${mins} minutos`;
      updateTimerDisplay();
      if (timerModal) timerModal.classList.add('open');
      startTimer();
    });
  });

  function updateTimerDisplay() {
    const m = Math.floor(timerSeconds / 60).toString().padStart(2, '0');
    const s = (timerSeconds % 60).toString().padStart(2, '0');
    if (timerDisplay) timerDisplay.textContent = `${m}:${s}`;
  }

  function startTimer() {
    if (timerRunning) return;
    timerRunning = true;
    timerInterval = setInterval(() => {
      if (timerSeconds <= 0) {
        clearInterval(timerInterval);
        timerRunning = false;
        if (timerDisplay) timerDisplay.textContent = '00:00';
        // Browser notification or vibration
        if (navigator.vibrate) navigator.vibrate([500, 200, 500]);
        window.showToast && window.showToast('⏰ Tempo esgotado!', 'success');
        if ('Notification' in window && Notification.permission === 'granted') {
          new Notification('⏰ Quero Rango', { body: 'Seu timer terminou!' });
        }
      } else {
        timerSeconds--;
        updateTimerDisplay();
      }
    }, 1000);
  }

  if (timerStart) timerStart.addEventListener('click', startTimer);

  if (timerPause) {
    timerPause.addEventListener('click', () => {
      if (timerRunning) {
        clearInterval(timerInterval);
        timerRunning = false;
        timerPause.textContent = '▶ Retomar';
      } else {
        startTimer();
        timerPause.textContent = '⏸ Pausar';
      }
    });
  }

  if (timerClose) {
    timerClose.addEventListener('click', () => {
      clearInterval(timerInterval);
      timerRunning = false;
      timerModal?.classList.remove('open');
    });
  }

  if (timerModal) {
    timerModal.addEventListener('click', e => {
      if (e.target === timerModal) {
        clearInterval(timerInterval);
        timerRunning = false;
        timerModal.classList.remove('open');
      }
    });
  }

  // ── Cooking Mode ───────────────────────────────────
  const cookingOverlay = document.getElementById('cooking-mode');
  const cookingText = document.getElementById('cooking-step-text');
  const cookingNum = document.getElementById('cooking-step-num');
  const cookingPrev = document.getElementById('cooking-prev');
  const cookingNext = document.getElementById('cooking-next');
  const cookingClose = document.getElementById('cooking-close');
  const cookingModeBtn = document.getElementById('start-cooking-mode');

  let cookingIndex = 0;
  const cookingSteps = [...document.querySelectorAll('.step-text')].map(el => el.textContent.trim());

  function updateCookingStep() {
    if (!cookingText || !cookingNum) return;
    cookingText.textContent = cookingSteps[cookingIndex] || '';
    cookingNum.textContent = `Passo ${cookingIndex + 1} de ${cookingSteps.length}`;
    if (cookingPrev) cookingPrev.disabled = cookingIndex === 0;
    if (cookingNext) cookingNext.textContent = cookingIndex === cookingSteps.length - 1 ? '🎉 Finalizar' : 'Próximo →';
  }

  if (cookingModeBtn && cookingOverlay) {
    cookingModeBtn.addEventListener('click', () => {
      cookingIndex = 0;
      updateCookingStep();
      cookingOverlay.classList.add('open');
      // Keep screen awake if supported
      if ('wakeLock' in navigator) {
        navigator.wakeLock.request('screen').catch(() => {});
      }
    });
  }

  if (cookingPrev) {
    cookingPrev.addEventListener('click', () => {
      if (cookingIndex > 0) { cookingIndex--; updateCookingStep(); }
    });
  }

  if (cookingNext) {
    cookingNext.addEventListener('click', () => {
      if (cookingIndex < cookingSteps.length - 1) {
        cookingIndex++;
        updateCookingStep();
      } else {
        cookingOverlay?.classList.remove('open');
        window.showToast && window.showToast('🎉 Receita finalizada! Bom apetite!', 'success');
      }
    });
  }

  if (cookingClose) {
    cookingClose.addEventListener('click', () => cookingOverlay?.classList.remove('open'));
  }

  // ── FAQ Accordion ──────────────────────────────────
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const answer = item.querySelector('.faq-answer');
      const isOpen = item.classList.contains('open');

      // Close all
      document.querySelectorAll('.faq-item.open').forEach(el => {
        el.classList.remove('open');
        el.querySelector('.faq-answer').style.maxHeight = '0';
      });

      // Open clicked if it was closed
      if (!isOpen) {
        item.classList.add('open');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });

  // ── Star Rating (interactive) ──────────────────────
  const starBtns = document.querySelectorAll('.star-btn');
  const ratingInput = document.getElementById('rating-input');
  const ratingText = document.getElementById('rating-text');

  const ratingLabels = ['', 'Ruim', 'Regular', 'Bom', 'Ótimo', 'Perfeito! 🎉'];

  starBtns.forEach(btn => {
    btn.addEventListener('mouseenter', () => highlightStars(parseInt(btn.dataset.value)));
    btn.addEventListener('mouseleave', () => {
      const current = parseInt(ratingInput?.value || 0);
      highlightStars(current);
    });
    btn.addEventListener('click', () => {
      const val = parseInt(btn.dataset.value);
      if (ratingInput) ratingInput.value = val;
      if (ratingText) ratingText.textContent = ratingLabels[val] || '';
      highlightStars(val);
      window.showToast && window.showToast(`⭐ Obrigado pela avaliação: ${ratingLabels[val]}!`);
    });
  });

  function highlightStars(count) {
    starBtns.forEach(btn => {
      const val = parseInt(btn.dataset.value);
      btn.textContent = val <= count ? '⭐' : '☆';
    });
  }

  // ── Question Form ──────────────────────────────────
  const questionForm = document.getElementById('question-form');
  if (questionForm) {
    questionForm.addEventListener('submit', e => {
      e.preventDefault();
      const nameEl = questionForm.querySelector('[name="name"]');
      const msgEl = questionForm.querySelector('[name="message"]');
      const name = nameEl?.value.trim();
      const msg = msgEl?.value.trim();
      if (!name || !msg) {
        window.showToast && window.showToast('⚠️ Preencha todos os campos');
        return;
      }
      // Simulate submission
      const btn = questionForm.querySelector('button[type="submit"]');
      if (btn) { btn.disabled = true; btn.textContent = 'Enviando...'; }
      setTimeout(() => {
        window.showToast && window.showToast('✅ Pergunta enviada com sucesso!', 'success');
        questionForm.reset();
        if (btn) { btn.disabled = false; btn.textContent = 'Enviar pergunta'; }
        // Add comment to list temporarily
        const list = document.getElementById('questions-list');
        if (list) {
          const item = document.createElement('div');
          item.className = 'question-item';
          item.style.cssText = 'background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:1rem;margin-bottom:.75rem;';
          item.innerHTML = `<strong>${name}</strong><span style="font-size:.75rem;color:var(--text-muted);margin-left:.5rem;">Agora</span><p style="margin-top:.5rem;font-size:.9rem;">${msg}</p>`;
          list.prepend(item);
        }
      }, 800);
    });
  }

  // ── Favorite button init ───────────────────────────
  const recipeId = document.getElementById('recipe-id')?.value;
  if (recipeId && window.updateFavBtn) window.updateFavBtn(recipeId);

  const favBtn = document.getElementById('fav-btn');
  if (favBtn && recipeId) {
    favBtn.addEventListener('click', () => {
      const title = document.getElementById('recipe-title')?.textContent || document.title;
      const url = window.location.href;
      const img = document.querySelector('.recipe-hero-img')?.src || '';
      window.toggleFavorite && window.toggleFavorite(recipeId, title, url, img);
    });
  }

})();
