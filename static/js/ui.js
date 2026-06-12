// Small UI utilities for micro-interactions
(function(){
  window.UI = {
    showSkeleton(containerSelector){
      const c = document.querySelector(containerSelector);
      if(!c) return;
      c.setAttribute('aria-busy','true');
      c.querySelectorAll('*').forEach(el=>el.classList.add('skeleton'));
    },
    hideSkeleton(containerSelector){
      const c = document.querySelector(containerSelector);
      if(!c) return;
      c.removeAttribute('aria-busy');
      c.querySelectorAll('*').forEach(el=>el.classList.remove('skeleton'));
    },
    // Simple focus helper to move focus to first focusable element inside a node
    focusFirst(container){
      const node = typeof container === 'string' ? document.querySelector(container) : container;
      if(!node) return;
      const focusable = node.querySelector('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      if(focusable) focusable.focus();
    }
  };
})();
