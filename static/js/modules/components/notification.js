//* Selectors
const notification = document.querySelector('.notifications');
const notificationButton = document.querySelector('.nav__notification');

//* Events listeners

// Add active class to notifications
notificationButton.addEventListener('click', () => notification.classList.add('active'));

// Remove active class from notifications
document.addEventListener('click', (e) => {
    if (!notification.contains(e.target) && !notificationButton.contains(e.target)) {
        notification.classList.remove('active');
    }
});