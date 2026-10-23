(function () {
  'use strict';
  function safeCell(value) {
    let text = String(value == null ? '' : value);
    if (/^[\s]*[=+@-]/.test(text) || /^[\t\r\n]/.test(text)) text = "'" + text;
    return '"' + text.replace(/"/g, '""') + '"';
  }
  function csv(rows) {
    return '\uFEFF' + rows.map(row => row.map(safeCell).join(',')).join('\r\n') + '\r\n';
  }
  function value(form, name) {
    const field = form.elements.namedItem(name);
    return field ? field.value.trim() : '';
  }
  function rowsFor(form) {
    const rows = [[document.querySelector('h1').textContent], ['현장명', value(form, 'project')], [form.dataset.tool === 'quote' ? '비교일' : '정리일', value(form, 'record_date')]];
    if (form.dataset.tool === 'photo') {
      rows.push(['항목', '확인할 자료', '자료 상태', '파일명·촬영 위치·메모']);
      form.querySelectorAll('.record-card').forEach((card, index) => {
        const i = index + 1;
        rows.push([card.querySelector('legend').textContent.replace(/^\d+/, '').trim(), card.querySelector('p').textContent, value(form, 'p'+i+'_state'), value(form, 'p'+i+'_note')]);
      });
    } else if (form.dataset.tool === 'quote') {
      rows.push(['구분', '견적 A', '견적 B']);
      [['업체명 또는 제안 별칭',''],['문서번호·제시일','_ref'],['DC·AC 용량 표기','_capacity'],['총액·세금 포함 표기','_price']].forEach(([label,suffix]) => rows.push([label,value(form,'quote_a'+suffix),value(form,'quote_b'+suffix)]));
      rows.push(['항목', '확인할 내용', '견적 A', '견적 B', '근거와 확인할 질문']);
      form.querySelectorAll('tbody tr').forEach((tr,index) => {
        const i = index+1, th = tr.querySelector('th');
        rows.push([th.firstChild.textContent.trim(),th.querySelector('.cell-note').textContent,value(form,'q'+i+'_a'),value(form,'q'+i+'_b'),value(form,'q'+i+'_note')]);
      });
    } else if (form.dataset.tool === 'change') {
      rows.push(['기록번호','변경 대상·구역','변경 전 문서번호·개정번호','변경 후 문서번호·개정번호','변경 전후 내용·이유·첨부자료 이름','확인 요청 대상·요청일','회신 문서명·회신일','문서관리 상태','회신 조건·미결 사항·반영 문서']);
      for (let i=1;i<=3;i++) rows.push(['id','subject','before','after','detail','request','reply','state','note'].map(key=>value(form,'c'+i+'_'+key)));
    }
    rows.push(['원본 페이지',location.origin+location.pathname]);
    return rows;
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = { safeCell, csv };
  if (typeof document === 'undefined') return;
  window.addEventListener('beforeprint', () => {
    document.querySelectorAll('.print-value').forEach(node => node.remove());
    document.querySelectorAll('form[data-tool] input, form[data-tool] textarea, form[data-tool] select').forEach(control => {
      const copy = document.createElement('span');
      copy.className = 'print-value';
      copy.textContent = control.value || '미기재';
      control.insertAdjacentElement('afterend', copy);
    });
  });
  window.addEventListener('afterprint', () => document.querySelectorAll('.print-value').forEach(node => node.remove()));
  document.querySelectorAll('form[data-tool]').forEach(form => {
    form.addEventListener('submit', event => event.preventDefault());
    const exportButton=form.querySelector('[data-export]'), printButton=form.querySelector('[data-print]'), message=form.querySelector('[data-status]');
    exportButton.hidden=false; printButton.hidden=false;
    exportButton.addEventListener('click', () => {
      try {
        const blob=new Blob([csv(rowsFor(form))],{type:'text/csv;charset=utf-8;'});
        const url=URL.createObjectURL(blob), link=document.createElement('a');
        link.href=url;link.download=form.dataset.filename;document.body.appendChild(link);link.click();link.remove();
        setTimeout(()=>URL.revokeObjectURL(url),30000);
        message.textContent='CSV 다운로드를 요청했습니다. 브라우저의 다운로드 목록에서 파일을 확인하세요.';
      } catch (error) {
        message.textContent='이 브라우저에서 파일을 만들지 못했습니다. 빈 CSV 양식을 내려받거나 인쇄 기능을 이용해 주세요.';
      }
    });
    printButton.addEventListener('click',()=>window.print());
  });
}());
