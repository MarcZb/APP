const btnDelete= document.querySelectorAll('.btn-delete');
if(btnDelete) {
  const btnArray = Array.from(btnDelete);
  btnArray.forEach((btn) => {
    btn.addEventListener('click', (e) => {
      if(!confirm('Are you sure you want to delete it?')){
        e.preventDefault();
      }
    });
  })
}

const btnApprove = document.querySelector('.btn-approve');
if (btnApprove) {
  btnApprove.addEventListener('click', (e) => {
    if (!confirm('Are you sure you want to approve?')) {
      e.preventDefault();
    }
  });
}
