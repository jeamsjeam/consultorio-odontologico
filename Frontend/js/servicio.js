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
                            <div class="card border-success mb-2" style="max-width: 18rem;">
                                <div class="card-header bg-transparent border-success text-danger">${data.nombre}</div>
                                    <div class="card-body">
                                        <p class="card-text">${data.descripcion}</p>
                                    </div>
                                <div class="card-footer bg-transparent border-success text-success">COP ${data.costo}</div>
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