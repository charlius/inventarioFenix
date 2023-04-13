const hamburgerBtn = document.getElementById('hamburgerBtn');
const navbarMenu = document.getElementById('navbarMenu');
const hamburgerIcon = document.getElementById('hamburgerIcon');
const closeIcon = document.getElementById('closeIcon');

hamburgerBtn.addEventListener('click', () => {
  navbarMenu.classList.toggle('hidden');
  if (navbarMenu.classList.contains('hidden')) {
    hamburgerIcon.style.display = 'block';
    closeIcon.style.display = 'none';
  } else {
    hamburgerIcon.style.display = 'none';
    closeIcon.style.display = 'block';
  }
});