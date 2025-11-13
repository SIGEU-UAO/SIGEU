//* Selectors
const navToggle = document.querySelector('.nav__toggle');
const navList = document.querySelector('.nav__list');
const navLink = document.querySelectorAll('.nav__link');
const navClose = document.querySelector('.nav__close'); 

//* Events
navToggle.addEventListener('click', () => {
    navList.classList.add('nav__list--active');
});

navLink.forEach(link => {
    link.addEventListener('click', () => {
        navList.classList.remove('nav__list--active');
    });
});

//* Close menu
navClose.addEventListener('click', () => {
    navList.classList.remove('nav__list--active');
});
