/** ---------------------------------------------------------------------
 * Logica.js
 *
 * 10/11/21
 *
 * Javier Solís
 *
 * Este fichero contiene todas las funciones que operan con sql y se
 * conectan a la bd
 *
 *
 * ------------------------------------------------------------------- */
//import sqlite3 from './node_modules/sqlites3'
const sqlite3 = require( "sqlite3")
// ---------------------------------------------------------------------
// ---------------------------------------------------------------------
module.exports = class Logica {
	
	// -----------------------------------------------------------------
	// nombreBD: Texto
	// -->
	//    constructor () -->
	// -----------------------------------------------------------------
	constructor( nombreBD, cb ) {
		this.laConexion = new sqlite3.Database(
			nombreBD,
			( err ) => {
				if( ! err ) {
					var context = this
					///////////////////////se pueden poner funciones y cosas así
					this.laConexion.run( "PRAGMA foreign_keys = ON" )
				}
				cb( err)
			}
		)
	} // ()

	// -----------------------------------------------------------------
	//	email, contrasenya: Texto
	// _getUsuarioConEmailYContrasenya() -->
	// email, nombre, id_invernadero, id_rol, contrasenya
	// -----------------------------------------------------------------
	_getUsuarioConEmail( email ){
		let textoSQL = "select * from Usuario where email=$email";
		let valoresParaSQL = { $email: email }
		return new Promise( (resolver, rechazar) => {
			this.laConexion.all( textoSQL, valoresParaSQL,
			( err, res ) => {
				if(err){
					rechazar(err)
				} else if(res.length > 1){
					rechazar("ERROR: mas de 1 usuario comparte email")
				} else if(res.length == 0){
					rechazar(404)
				} else {
					resolver(res[0])
				}
			})
		})
	}
	
	// -----------------------------------------------------------------
	//	email: Texto
	// _getUsuarioConEmailYContrasenya() -->
	// contrasenya
	// -----------------------------------------------------------------
	_comprobarContrasenyaConEmailYContrasenya( email, contrasenya ){
		let textoSQL = "select Contrasenya from Usuario where email=$email and contrasenya=$contrasenya";
		let valoresParaSQL = { $email: email, $contrasenya: contrasenya }
		return new Promise( (resolver, rechazar) => {
			this.laConexion.all( textoSQL, valoresParaSQL,
			( err, res ) => {
				if(err){
					rechazar(err)
				} else if(res.length > 1){
					rechazar("ERROR: mas de 1 usuario comparte email")
				} else if(res.length == 0){
					rechazar(404)
				} else {
					resolver(res[0])
				}
			})
		})
	}

	// -----------------------------------------------------------------
	//	email: Texto
	// _getUsuarioConEmailYContrasenya() -->
	// contrasenya
	// -----------------------------------------------------------------
	_cambiarContrasenya( contrasenya, email ){
		let textoSQL = "UPDATE Usuario SET contrasenya = $contrasenya where email=$email";
		let valoresParaSQL = { $email: email, $contrasenya: contrasenya }
		return new Promise( (resolver, rechazar) => {
			this.laConexion.all( textoSQL, valoresParaSQL,
			( err, res ) => {
				if(err){
					rechazar(err)
				} else if(res.length > 1){
					rechazar("ERROR: mas de 1 usuario comparte email")
				} else if(res.length == 0){
					rechazar(404)
				} else {
					resolver(res[0])
				}
			})
		})
	}

	// -----------------------------------------------------------------
	//	email: Texto
	// _getUsuarioConEmail() -->
	// email, nombre, id_invernadero, id_rol, contrasenya
	// -----------------------------------------------------------------

	_getUsuarioConEmailYContrasenya( email, contrasenya ){
		let textoSQL = "select * from Usuario where email=$email and contrasenya=$contrasenya";
		let valoresParaSQL = { $email: email, $contrasenya: contrasenya }
		return new Promise( (resolver, rechazar) => {
			this.laConexion.all( textoSQL, valoresParaSQL,
			( err, res ) => {
				if(err){
					rechazar(err)
				} else if(res.length > 1){
					rechazar("ERROR: mas de 1 usuario comparte email")
				} else if(res.length == 0){
					rechazar(404)
				} else {
					resolver(res[0])
				}
			})
		})
	}

	// -----------------------------------------------------------------
	// cerrar() -->
	// -----------------------------------------------------------------
	cerrar() {
		return new Promise( (resolver, rechazar) => {
			this.laConexion.close( (err)=>{
				( err ? rechazar(err) : resolver(200) )
			})
		})
	} // ()
} // class
// ---------------------------------------------------------------------
// ---------------------------------------------------------------------
