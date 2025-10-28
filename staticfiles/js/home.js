
  const cards = document.querySelectorAll('.info-cards .card');
  let current = 0;

  function showNextCard() {
    cards.forEach((card, index) => {
      card.classList.remove('active');
    });
    cards[current].classList.add('active');
    current = (current + 1) % cards.length;
  }

  // Démarre l'animation
  showNextCard();
  setInterval(showNextCard, 5000); // change toutes les 2 secondes

