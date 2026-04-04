/**
 * Scroll-triggered animations for Jarvis site
 * Respects prefers-reduced-motion setting
 */

(function() {
  'use strict';

  // Early return if reduced motion is preferred
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    return;
  }

  // Intersection Observer options
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  // Create observer
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, observerOptions);

  // Initialize animations when DOM is ready
  function initAnimations() {
    // Find all elements to animate
    const animateElements = document.querySelectorAll(
      '.card, .project, .cta-button, .hero, .emotional-section, h2, h3, .intro, .callout, .tldr'
    );

    // Add animation classes and observe
    animateElements.forEach((el, index) => {
      // Add base animation class with slight delay
      el.style.animationDelay = `${index * 100}ms`;
      
      // Determine animation type based on element
      if (el.matches('.hero, .emotional-section')) {
        el.classList.add('slide-up');
      } else {
        el.classList.add('fade-in');
      }
      
      // Start observing
      observer.observe(el);
    });
  }

  // Wait for DOM to be ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAnimations);
  } else {
    initAnimations();
  }

  // Smooth scroll for anchor links
  document.addEventListener('click', (e) => {
    const link = e.target.closest('a');
    if (!link) return;

    const href = link.getAttribute('href');
    if (href && href.startsWith('#')) {
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    }
  });

  // Add loading animation to CTA buttons
  document.addEventListener('click', (e) => {
    const cta = e.target.closest('.cta-button, .whatsapp-cta');
    if (cta && !cta.classList.contains('loading')) {
      cta.classList.add('loading');
      setTimeout(() => {
        cta.classList.remove('loading');
      }, 1000);
    }
  });

})();