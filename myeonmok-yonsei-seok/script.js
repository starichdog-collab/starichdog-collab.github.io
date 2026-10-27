(() => {
  'use strict';
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#main-nav');
  const closeMenu = () => {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-label', '메뉴 열기');
    nav.classList.remove('is-open');
  };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
    nav.classList.toggle('is-open', open);
  });
  nav.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      toggle.focus();
    }
  });
  window.matchMedia('(min-width: 901px)').addEventListener('change', closeMenu);

  const copyButton = document.querySelector('[data-copy-address]');
  const toast = document.querySelector('.toast');
  let toastTimeout;
  function notify(message) {
    toast.textContent = message;
    toast.classList.add('visible');
    window.clearTimeout(toastTimeout);
    toastTimeout = window.setTimeout(() => toast.classList.remove('visible'), 4200);
  }
  copyButton.addEventListener('click', async () => {
    const address = '서울특별시 중랑구 면목로 398 스마트빌딩 (외래 2층, 인공신장실 5·6층)';
    try {
      if (!navigator.clipboard || !window.isSecureContext) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(address);
      notify('병원 주소를 복사했습니다.');
    } catch {
      const input = document.createElement('textarea');
      input.value = address;
      input.setAttribute('readonly', '');
      input.style.cssText = 'position:fixed;left:-9999px;top:0;';
      document.body.appendChild(input);
      input.select();
      let copied = false;
      try { copied = document.execCommand('copy'); } catch { /* Use visible address selection below. */ }
      input.remove();
      copyButton.focus();
      if (copied) {
        notify('병원 주소를 복사했습니다.');
      } else {
        const range = document.createRange();
        range.selectNodeContents(document.querySelector('#clinic-address'));
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        notify('주소를 선택했습니다. 길게 누르거나 복사해 주세요.');
      }
    }
  });
})();
