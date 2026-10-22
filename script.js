'use strict';
// Progressive enhancement only: every page works without JavaScript.

// Header gets a hairline once the page scrolls.
const header = document.querySelector('.site-header');
if (header) {
  const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 8);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
}

// Highlight the nav item (home page) or table-of-contents item (case pages)
// for the section currently in view.
function trackSections(links, getTarget) {
  if (!('IntersectionObserver' in window) || !links.length) return;
  const map = new Map();
  links.forEach(link => {
    const target = getTarget(link);
    if (target) map.set(target, link);
  });
  const visible = new Set();
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => (entry.isIntersecting ? visible.add(entry.target) : visible.delete(entry.target)));
    const first = [...map.keys()].find(section => visible.has(section));
    links.forEach(link => link.classList.toggle('active', first ? map.get(first) === link : false));
  }, { rootMargin: '-30% 0px -60% 0px' });
  map.forEach((_, section) => observer.observe(section));
}

const isHome = !!document.querySelector('.hero');
if (isHome) {
  trackSections([...document.querySelectorAll('.site-nav a[href^="#"]')], link => document.querySelector(link.getAttribute('href')));
}
trackSections([...document.querySelectorAll('.toc a')], link => document.querySelector(link.getAttribute('href')));

// Copy email.
document.querySelectorAll('[data-copy-email]').forEach(button => {
  button.addEventListener('click', async () => {
    const status = document.getElementById('copy-status');
    const email = button.dataset.copyEmail;
    try {
      await navigator.clipboard.writeText(email);
      if (status) status.textContent = `Copied ${email} to the clipboard.`;
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = 'Copy email'; }, 2400);
    } catch {
      if (status) status.textContent = `Couldn’t copy automatically. The address is ${email}.`;
    }
  });
});

// Print (resume page).
document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));

// Keep the footer year current.
document.querySelectorAll('[data-year]').forEach(el => { el.textContent = String(new Date().getFullYear()); });

// The toggle that stands in for the "O" in SOFTWARE: flip the bit.
document.querySelectorAll('[data-toggle]').forEach(toggle => {
  toggle.addEventListener('click', () => {
    toggle.setAttribute('aria-pressed', String(toggle.getAttribute('aria-pressed') !== 'true'));
  });
});

// SVG (SMIL) animations ignore CSS, so pause them for people who prefer less motion.
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.querySelectorAll('svg').forEach(svg => { if (svg.pauseAnimations) svg.pauseAnimations(); });
}
