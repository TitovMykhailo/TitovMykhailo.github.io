'use strict';

// Progressive enhancement: all project text and links exist in the HTML.
const filterButtons = document.querySelectorAll('[data-filter]');
filterButtons.forEach(button => {
  button.addEventListener('click', () => {
    const category = button.dataset.filter;
    let count = 0;
    filterButtons.forEach(item => {
      const active = item === button;
      item.classList.toggle('active', active);
      item.setAttribute('aria-pressed', String(active));
    });
    document.querySelectorAll('[data-category]').forEach(project => {
      project.hidden = category !== 'all' && project.dataset.category !== category;
      if (!project.hidden) count++;
    });
    const announcement = document.getElementById('filter-status');
    if (announcement) announcement.textContent = `Showing ${count} ${count === 1 ? 'project' : 'projects'}.`;
  });
});

document.querySelectorAll('[data-copy-email]').forEach(button => {
  button.addEventListener('click', async () => {
    const announcement = document.getElementById('copy-status');
    try {
      await navigator.clipboard.writeText(button.dataset.copyEmail);
      if (announcement) announcement.textContent = 'Email address copied.';
    } catch {
      if (announcement) announcement.textContent = `Copy this address: ${button.dataset.copyEmail}`;
    }
  });
});

document.querySelectorAll('[data-print]').forEach(button => {
  button.addEventListener('click', () => window.print());
});

// Never hide content unless observation is supported. Reduced motion stays static.
if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.06 });
  document.documentElement.classList.add('reveal-ready');
  document.querySelectorAll('.reveal').forEach(element => observer.observe(element));
}

document.querySelectorAll('[data-year]').forEach(element => {
  element.textContent = String(new Date().getFullYear());
});
