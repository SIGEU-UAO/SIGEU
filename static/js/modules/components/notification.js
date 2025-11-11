import API from "../classes/API.js";
import Alert from "../classes/Alert.js";

//* Selectors
const notification = document.querySelector('.notifications');
const notificationButton = document.querySelector('.nav__notification');
const notificationCards = document.querySelector('.notifications__content');
const notificationsReadButtons = document.querySelectorAll('.notification__card__read');
const notificationEmpty = document.querySelector('.notifications__empty');

// Add active class to notifications
notificationButton.addEventListener('click', () => notification.classList.add('active'));

// Remove active class from notifications
document.addEventListener('click', (e) => {
    if (!notification.contains(e.target) && !notificationButton.contains(e.target)) {
        notification.classList.remove('active');
    }
});

// Mark as read a notification
notificationsReadButtons.forEach(button => {
    button.addEventListener('click', (e) => markAsRead(e));
});

//* Functions
async function markAsRead(e) {
    const markAsReadBtn = e.target.nodeName !== "I" ? e.target : e.target.parentElement;
    const notificationCard = markAsReadBtn.parentElement.parentElement;
    const evaluationId = markAsReadBtn.dataset.id;
    const response = await API.patch(`/eventos/api/marcar-notificacion-como-leida/${evaluationId}/`);
    if(response.error) return;
    notificationCard.remove();
    Alert.success("Notificación marcada como leída");
    // It's 1 because the empty message is also a child element
    if (notificationCards.childElementCount === 1) changeBellStatus();
}

function changeBellStatus() {
    notificationButton.classList.toggle('new');
    notificationEmpty.classList.toggle('show');
}