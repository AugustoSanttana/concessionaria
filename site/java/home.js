const track = document.querySelector('.carousel-track');
const next = document.querySelector('.next');
const prev = document.querySelector('.prev');

next.addEventListener('click', () => {
  track.scrollBy({ left: 300, behavior: 'smooth' });
});

prev.addEventListener('click', () => {
  track.scrollBy({ left: -300, behavior: 'smooth' });
});