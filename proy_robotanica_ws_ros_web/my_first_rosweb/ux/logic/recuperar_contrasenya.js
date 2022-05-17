// ---------------------------------------------------------------------
// LogicaFake.js
// ---------------------------------------------------------------------

const IP_PUERTO = "http://localhost:8080";
// ---------------------------------------------------------------------
// ---------------------------------------------------------------------
export default class recuperar_contrasenya {

    /*email, contrasenya, confirmacion {Texto} ->
      buscarUsuarioConEmail() ->
      -------------------------------------------
      Declaramos esta función, con una petición GET al servicio REST, para comprobar que exista dicho usuario con dicha contrasenya.
      En el caso de que encuentre uno, llamara a la funcion de cambiar contrasenya
    */
    async buscarUsuarioConEmail(email, contrasenya, confirmacion) {
        console.log(email)
        var metodo = this;
        if (email == "" || contrasenya == "" || contrasenya!=confirmacion) return;

        let peticion = await fetch(IP_PUERTO + '/contrasenya/' + email + '/' + contrasenya, {
            method: 'GET'
        });
        if (peticion.status == 404) {
            let message = document.getElementById("contrasenyaIncorrecta")
            message.innerHTML = "Email o contraseña incorrectos";
            return;
        } else {
			cambiarContrasenya(email, contrasenya);
            
        }
        
    }

    /*email, contrasenya {Texto} ->
      cambiarContrasenya() ->
      ------------------------------
      Declaramos esta función, con una petición POST al servicio REST, para actualizar la tabla de Usuario
      con la nueva información
    */
    async cambiarContrasenya(email, contrasenya) {
        console.log(email + " / " + contrasenya)
        var metodo = this;
        if (contrasenya == "") return;

        let peticion = await fetch(IP_PUERTO + '/nueva_contrasenya/' + email + '/' + contrasenya, {
            method: 'POST'
        });
        if (peticion.status == 404) {
            
            return;
        } else {
			
            
        }
        
    }

}
// ---------------------------------------------------------------------
// ---------------------------------------------------------------------
