var show = document.querySelector('#show');
show.addEventListener('click', function() {
  login.showModal();
  console.log('dialog opened');
});
show.addEventListener('close', function() {
  console.log('dialog closed');
});
show.addEventListener('cancel', function() {
  console.log('dialog canceled');
});
var close = login.querySelector('#close');
close.addEventListener('click', function() {
  login.close();
});