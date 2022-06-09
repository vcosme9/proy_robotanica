// ---------------------------------------------------------------------
// LogicaGaleria.js
// ---------------------------------------------------------------------

const IP_PUERTO = "http://localhost:8080";
var coleccion_entera = [];
// ---------------------------------------------------------------------
// ---------------------------------------------------------------------
export default class LogicaGaleria {
	
	async init(){
		
		var metodo = this
		let peticion;
		
		let email = localStorage.getItem('email')

		peticion = await fetch(IP_PUERTO + '/galeria/' + email, {
			method: 'GET'
		});
		
		if (peticion.status != 404) {
			peticion.json().then(function (contenido) {
				coleccion_entera = contenido;
				metodo.llenarTabla(coleccion_entera)
				return;
			});
		}
		
		let vacio = []
		metodo.llenarTabla(vacio)
		return

	}
	
	llenarTabla(lista) {
		
		const tablaBody = document.getElementById("body-tabla");

        tablaBody.innerHTML = "";
		
		let textoBorrar = document.getElementById("textoBorrar")
		let tr, td, img, p, url, fecha, seccion;
		var email, error;
		let j = 0;
		
		if(lista.length != 0){
			for(j=0;j<lista.length;j++){
				
				url = lista[j]["url"]
				fecha = lista[j]["fecha"]
				seccion = lista[j]["seccion"]

				if(fecha == undefined) fecha = "--/--/----"
				
				tr = document.createElement("tr");
				tr.id = "contenedor_url_"+j;
				tr.classList.add("text-center")
				
				td = document.createElement("td")
				td.id = "url_" + j
				td.setAttribute("style", "padding: 40px;")
				
				img = document.createElement("img")
				img.id = "img" + j
				img.style.width = "320px"
				img.style.height = "240px"
				img.src = url
				
				td.append(img)
				tr.append(td)
				
				td = document.createElement("td")
				td.id = "contenedor_seccion_"+j
				td.setAttribute("style", "padding-top: 40px;")
				
				p = document.createElement("p")
				p.id = "seccion_"+j
				p.setAttribute("style", "font-weight: bold;")
				p.innerHTML=seccion
				
				td.append(p)
				tr.append(td)
				
				td = document.createElement("td")
				td.id = "contenedor_fecha_"+j
				td.setAttribute("style", "padding-top: 40px;")
				
				p = document.createElement("p")
				p.id = "fecha_"+j
				p.setAttribute("style", "font-weight: bold;")
				p.innerHTML=fecha
				
				td.append(p)
				tr.append(td)
				
				tablaBody.appendChild(tr);
			}
		} else {
             /** Nuevo td */
			let p;
            td = document.createElement("td");
            td.colSpan = 2;
            /** Nuevo p */
            p = document.createElement("p");
            p.classList.add("text-danger");
            p.classList.add("p-5");
            p.innerHTML = "No hay fotos que cumplan los requisitos establecidos.";
            /** Añade tr a tablaBody */
            td.appendChild(p);
            tablaBody.appendChild(td);
        }
		
    }
	
	/*
		Filtra la colección según el tipo de cultivo
	*/
	filtrar_tipo(coleccion, tipo){
		
		let nueva_coleccion = []
		
		let foto
		
		for (let i = 0; i < coleccion.length; i++){
			foto = coleccion[i]
			if(foto.seccion == tipo){
				nueva_coleccion.push(foto)
			}
		}
		
		return nueva_coleccion
		
	}
	
	/*
		Filtra la colección según la fecha
	*/
	filtrar_fecha(coleccion, fecha_1, fecha_2){
		
		let fecha_inicio = this.convertir_dia(new Date(fecha_1))
		let fecha_final = this.convertir_dia(new Date(fecha_2))
		let nueva_coleccion = []
		let fecha_evaluada, foto
		
		for (let i = 0; i < coleccion.length; i++){
			foto = coleccion[i]
			fecha_evaluada = this.convertir_dia(new Date(foto.fecha))

			if(fecha_evaluada >= fecha_inicio && fecha_evaluada <= fecha_final){
				nueva_coleccion.push(foto)
			}
			
		}
		
		return nueva_coleccion
		
	}
	
	/*
		Actualiza la tabla según los parámetros pasados por le usuario
	*/
	actualizar_tabla(fecha_inicio, fecha_final, tipo){
		
		let date = this.convertir_dia()
		let caso = 1
		let nueva_coleccion = coleccion_entera
		
		//si alguna de las fechas no está definida, no filtrará por fecha
		if(fecha_inicio + "" == "" || fecha_final + "" == ""){
			caso = 0
		}
		
		//si tiene algún tipo definido, filtrará por tipo
		if(tipo != "Todos") caso += 2
		
		/*
		si caso 0, solo actualizo
		si caso 1, entre fechas
		si caso 2, con tipo
		si caso 3, todo
		*/
		switch(caso){
			case 1:
				nueva_coleccion = this.filtrar_fecha(coleccion_entera, fecha_inicio, fecha_final)
				break
			case 2:
				nueva_coleccion = this.filtrar_tipo(coleccion_entera, tipo)
				break;
			case 3:
				nueva_coleccion = this.filtrar_fecha(coleccion_entera, fecha_inicio, fecha_final)
				nueva_coleccion = this.filtrar_tipo(nueva_coleccion, tipo)
				break
			default:
				break
		}
		
		this.llenarTabla(nueva_coleccion)
		
		return
		
	}
	
	convertir_dia(date = new Date()){
		let d = date.getDate()
		let sd = d
		if(d < 10) sd = "0" + d
		let m = date.getMonth()+1
		let sm = m
		if(m < 10) sm = "0" + m
		var date = date.getFullYear()+'-'+sm+'-'+sd;
		return date
	}

}