const nav = document.querySelector('nav');
const toggleButton = document.querySelector('button');

toggleButton.addEventListener('click', () => {
  nav.classList.toggle('open');
});