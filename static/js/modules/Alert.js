const notyf = new Notyf({
    position: { x: 'right', y: 'top' }
});

export default class Alert {
    static success(message) {
        notyf.success(message);
    }   
    static error(message) {
        notyf.error(message);
    }
}