document.addEventListener('DOMContentLoaded', async function() {
	await cargarServicios()
});

async function cargarServicios(){
    try{
        let datos = await consultar('servicio', 'GET', null); 

        if(typeof datos === 'undefined' || datos === null || datos.length === 0){
			mostrarNotificacion("No se encontro ningun servicio","#FF0000") 
			return
		}

        let contenido = ''

        for(const data of datos){
            contenido += `<div class="col">
 
                            <div class="card">
                            <img src="imagenes/${data.imagen}.jpg" class="card-img-top" alt="">
                                <div class="card-body">
                                    <h5 class="card-title text-danger">${data.nombre}</h5>
                                    <p class="card-text">${data.descripcion}</p>
                                    <p class="card-text text-succes">${data.costo}</p>
                                </div>
                            </div>
                        </div>`
        }

        document.getElementById("servicios").innerHTML = contenido;
        mostrarNotificacion("Servicios Encontrados","linear-gradient(to right, #00b09b, #96c93d)"); 

    }catch(e){
		mostrarNotificacion("Error: " + e,"#FF0000")  
		console.error('Error:', e);
	}
}