document.addEventListener('DOMContentLoaded', function() {
  const filterForm = document.getElementById('wf-form-Filter-2');
  
  // 個別のクリアボタンの取り扱い
  document.querySelectorAll('.clear-filter').forEach(button => {
      button.addEventListener('click', function(e) {
          e.preventDefault();
          const filterType = this.dataset.filter;
          document.querySelectorAll(`input[name="${filterType}"]`).forEach(checkbox => {
              checkbox.checked = false;
          });
          filterForm.submit();
      });
  });
  
  // 全消去ボタンの取り扱い
  document.querySelector('.clear-all-filters').addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelectorAll('.filter-checkbox').forEach(checkbox => {
          checkbox.checked = false;
      });
      filterForm.submit();
  });
  
  // チェックボックスの変更時にフォームを自動的に送信
  document.querySelectorAll('.filter-checkbox').forEach(checkbox => {
      checkbox.addEventListener('change', () => {
          filterForm.submit();
      });
  });

  // ソートオプションの取り扱い
  document.querySelectorAll('.dropdown1_dropdown-link').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const sortField = this.getAttribute('fs-cmssort-field');
        const sortInput = document.createElement('input');
        sortInput.type = 'hidden';
        sortInput.name = 'sort';
        sortInput.value = sortField;
        filterForm.appendChild(sortInput);
        filterForm.submit();
    });
  });
});