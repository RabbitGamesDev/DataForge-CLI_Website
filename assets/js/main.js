// DataForge CLI — shared site behavior (no frameworks, no build step)

// --- AUTO-INJECT GOOGLE TRANSLATE WIDGET ---
window.googleTranslateElementInit = function() {
    new google.translate.TranslateElement({
        pageLanguage: 'es',
        includedLanguages: 'es,en',
        layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
        autoDisplay: false
    }, 'google_translate_element');
};

document.addEventListener('DOMContentLoaded', () => {

  // 1. Inicializar contenedor y script de Google Translate de forma invisible/automática
  const translateDiv = document.createElement('div');
  translateDiv.id = 'google_translate_element';
  translateDiv.style.display = 'none';
  document.body.appendChild(translateDiv);

  const script = document.createElement('script');
  script.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
  document.head.appendChild(script);

  /* Mobile nav toggle */
  const toggle = document.querySelector('.nav-toggle');
  const links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => {
      const open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => links.classList.remove('open'));
    });
  }

  /* Mark active nav link based on current page */
  const current = (location.pathname.split('/').pop() || 'index.html');
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href');
    if (href === current || (current === '' && href === 'index.html')) {
      a.classList.add('active');
    }
  });

  /* Scroll reveal */
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('in'));
  }

  /* Copy-to-clipboard for terminal / code snippets */
  document.querySelectorAll('.code-block').forEach(block => {
    const btn = block.querySelector('.copy-btn');
    const codeEl = block.querySelector('code') || block;
    if (!btn) return;
    btn.addEventListener('click', async () => {
      const text = codeEl.innerText.trim();
      try {
        await navigator.clipboard.writeText(text);
      } catch (e) {
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      }
      btn.classList.add('copied');
      const original = btn.getAttribute('data-label') || '';
      btn.setAttribute('aria-label', 'Copiado');
      setTimeout(() => {
        btn.classList.remove('copied');
        btn.setAttribute('aria-label', original || 'Copiar');
      }, 1600);
    });
  });

  /* FAQ accordion */
  document.querySelectorAll('.faq-item').forEach(item => {
    const q = item.querySelector('.faq-q');
    if (!q) return;
    q.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');
      item.classList.toggle('open', !isOpen);
      q.setAttribute('aria-expanded', !isOpen ? 'true' : 'false');
    });
  });

  /* Pricing toggle: monthly / annual (if present) */
  const pricingToggle = document.querySelector('.pricing-toggle');
  if (pricingToggle) {
    const priceEls = document.querySelectorAll('[data-price-monthly]');
    pricingToggle.addEventListener('change', (e) => {
      const annual = e.target.checked;
      priceEls.forEach(el => {
        el.textContent = annual ? el.dataset.priceAnnual : el.dataset.priceMonthly;
      });
      document.querySelectorAll('.price-period').forEach(el => {
        const monthly = el.dataset.periodMonthly || '/mes';
        const annualLabel = el.dataset.periodAnnual || (monthly + ', facturado anual');
        el.textContent = annual ? annualLabel : monthly;
      });
    });
  }

  /* Docs search filter (simple client-side filter over .doc-command cards) */
  const docSearch = document.getElementById('doc-search');
  if (docSearch) {
    const cards = document.querySelectorAll('.doc-command');
    docSearch.addEventListener('input', () => {
      const q = docSearch.value.trim().toLowerCase();
      cards.forEach(card => {
        const text = card.innerText.toLowerCase();
        card.style.display = text.includes(q) ? '' : 'none';
      });
    });
  }

});
