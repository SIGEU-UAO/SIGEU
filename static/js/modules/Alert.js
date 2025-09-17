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

    static showPasswordInfo(){
        Swal.fire({
            icon: "info",  // mejor usar info para indicar reglas, no error
            title: "Restricciones de la contraseña",
            html: `
                <ul style="text-align:center; list-style:none">
                    <li>Mínimo 8 caracteres</li>
                    <li>Al menos una letra mayúscula</li>
                    <li>Al menos una letra minúscula</li>
                    <li>Al menos un número</li>
                </ul>
            `,
            confirmButtonText: "Entendido",
            confirmButtonColor: "#FF7AA2"
        });
    }
}