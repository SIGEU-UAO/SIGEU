const notyf = new Notyf({
    position: { x: 'right', y: 'top' },
    types: [
      {
        type: 'info',
        background: '#3498db', 
        icon: {
          className: 'ri-information-fill', 
          tagName: 'i',                    
          color: 'white'                     
        }
      },
      {
        type: 'warning',
        background: '#ff8921',
        icon: {
          className: 'ri-alert-fill',
          tagName: 'i',
          color: 'white'
        }
      }
    ]
});

export default class Alert {
    static success(message) {
        notyf.success(message);
    }   
    
    static error(message) {
        notyf.error(message);
    }
    
    static info(message) {
        notyf.open({
            type: 'info',
            message: message
        });
    }

    static warning(message) {
        notyf.open({
            type: 'warning',
            message: message
        });
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

    static async confirmationAlert({title, text, confirmButtonText = "Aceptar", cancelButtonText = "Cancelar"}) {
        return await Swal.fire({title, 
            text, 
            showCancelButton: true, 
            confirmButtonText,
            cancelButtonText,
            confirmButtonColor: "#ff7aa2",
            cancelButtonColor: "#666666",
            reverseButtons: true
    });
}
}

