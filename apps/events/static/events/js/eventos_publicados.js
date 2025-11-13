//* Selectores
const cardsContainer = document.querySelector('.cards');
const noResultsContainer = document.querySelector('.no-results-container');
noResultsContainer.style.display = cardsContainer.children.length === 0 ? 'flex' : 'none';