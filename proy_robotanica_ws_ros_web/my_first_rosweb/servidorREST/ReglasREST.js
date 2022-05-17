//----------------------------------------------------------------------
// ReglasREST.js
//----------------------------------------------------------------------
module.exports.cargar = function( servidorExpress, laLogica ) {
	//--------------------------------------------------------
	// GET /prueba
	//--------------------------------------------------------
	servidorExpress.get('/prueba/', function( peticion, respuesta ){
		console.log( " * GET /prueba " )
		respuesta.send( "¡Funciona!" )
	}) // get /prueba
	
	
//////////////////////////////////////////////////////////////
// MÉTODO GET
//////////////////////////////////////////////////////////////
	
	//--------------------------------------------------------
	// Peticion GET /usuario/:email/:contrasenya
	//--------------------------------------------------------
	servidorExpress.get(
		'/usuario/:email/:contrasenya',
		async function(peticion, respuesta) {
			console.log(" * GET /usuario ")
				// averiguo el email y la contrasenya
			var email = peticion.params.email
			var contrasenya = peticion.params.contrasenya
				// llamo a la función adecuada de la lógica
			var res = null
			var error = null

			try {
				res = await laLogica._getUsuarioConEmailYContrasenya(email, contrasenya)
			} catch (e) {
				error = e
			}
			// si el array de resultados no tiene una casilla ...
			if (error != null) {
				if (error == 404) {
					respuesta.status(404).send("No encontré usuario con email " + email + " y contrasenya " + contrasenya)
				} else {
					//500: internal server error
					console.log(error)
					respuesta.status(500).send("Error interno del servidor")
				}
				return
			} else {
				respuesta.send(JSON.stringify(res))
			}
		}) // get /usuario

		servidorExpress.get(
			'/contrasenya/:email/:contrasenya',
			async function(peticion, respuesta) {
				console.log(" * GET /contrasenya ")
					// averiguo el email y la contrasenya
				var email = peticion.params.email
				var contrasenya = peticion.params.contrasenya
					// llamo a la función adecuada de la lógica
				var res = null
				var error = null
	
				try {
					res = await laLogica._comprobarContrasenyaConEmailYContrasenya(email,contrasenya)
				} catch (e) {
					error = e
				}
				// si el array de resultados no tiene una casilla ...
				if (error != null) {
					if (error == 404) {
						respuesta.status(404).send("No encontré usuario con email " + email)
					} else {
						//500: internal server error
						console.log(error)
						respuesta.status(500).send("Error interno del servidor")
					}
					return
				} else {
					respuesta.send(JSON.stringify(res))
				}
			}) // get /contrasenya

			servidorExpress.post(
				'/nueva_contrasenya/:email/:contrasenya',
				async function(peticion, respuesta) {
					console.log(" * POST /contrasenya ")
						// averiguo el email y la contrasenya
					var email = peticion.params.email
					var contrasenya = peticion.params.contrasenya

						// llamo a la función adecuada de la lógica
					var res = null
					var error = null
		
					try {
						res = await laLogica._cambiarContrasenya(email,contrasenya)
					} catch (e) {
						error = e
					}
					// si el array de resultados no tiene una casilla ...
					if (error != null) {
						if (error == 404) {
							respuesta.status(404).send("No encontré usuario con email " + email)
						} else {
							//500: internal server error
							console.log(error)
							respuesta.status(500).send("Error interno del servidor")
						}
						return
					} else {
						respuesta.send(JSON.stringify(res))
					}
				}) // get /usuario
	
}
//----------------------------------------------------------------------
//----------------------------------------------------------------------
