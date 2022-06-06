// ---------------------------------------------------------------------
// LogicaFake.js
// ---------------------------------------------------------------------

const IP_PUERTO = "http://localhost:8080";
// ---------------------------------------------------------------------
// ---------------------------------------------------------------------
export default class LogicaFakeLogIn {

    async buscarUsuarioConEmailYContrasenya(email, contrasenya) {
        console.log(email + " / " + contrasenya)
        var metodo = this;
        if (email == "" || contrasenya == "") return;

        let peticion = await fetch(IP_PUERTO + '/usuario/' + email + '/' + contrasenya, {
            method: 'GET'
        });
        if (peticion.status == 404) {
            let message = document.getElementById("contrasenyaIncorrecta")
            message.innerHTML = "Email o contraseña incorrectos";
            return;
        } else {
			
			//guardo el email para recuperar la información de este usuario más adelante
			localStorage.setItem('email', email)
			window.open("./funcionalidades.html", "_self")
            
        }
        
    }
}
// ---------------------------------------------------------------------
// ---------------------------------------------------------------------
