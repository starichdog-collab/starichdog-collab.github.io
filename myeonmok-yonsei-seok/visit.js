(() => {
  'use strict';
  const form = document.querySelector('[data-visit-checklist]');
  if (!form) return;
  const boxes = [...form.querySelectorAll('input[type="checkbox"]')];
  const output = form.querySelector('[data-checklist-progress]');
  const update = () => {
    const count = boxes.filter(box => box.checked).length;
    output.textContent = count ? `${count}개 항목을 확인했습니다. 해당하는 항목만 확인하세요.` : '방문 목적에 해당하는 항목을 눌러 확인하세요.';
  };
  form.addEventListener('submit', event => event.preventDefault());
  form.addEventListener('change', update);
  form.addEventListener('reset', () => { window.setTimeout(update, 0); });
  form.querySelector('[data-print-checklist]').addEventListener('click', () => window.print());
  update();
})();
