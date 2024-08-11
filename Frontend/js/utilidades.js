document.addEventListener("DOMContentLoaded", async function () {

    // Se valida si la ruta no es index, registro o recuperacion
    if (window.location.href.indexOf('login.html') === -1 && 
        window.location.href.indexOf('registro.html') === -1 &&
        window.location.href.indexOf('recuperacion.html') === -1) {

        // Se carga el navbar y se crea el html de los modales
        CargarNavbar(window.location.href);
        CrearModales();

        // Se verifica si existe usuario en el sessionStorage
        //En caso de no existir se redigire al login 
        let datosUsuario = sessionStorage.getItem('usuario');
        if (typeof datosUsuario === 'undefined' || datosUsuario === null) {
            window.location.href = "login.html";
        }

        //Se verifica si no ex el index
        if (window.location.href.indexOf('index.html') !== -1) {

            // Se verifica si existe usarioLogeado, para poder mostrar una notificacion en verde
            let usuarioLogeado = JSON.parse(localStorage.getItem('usuarioLogeado'));
            if (typeof usuarioLogeado !== 'undefined' &&  usuarioLogeado !== null && typeof usuarioLogeado.usuario !== 'undefined' && usuarioLogeado.usuario !== null) {
                mostrarNotificacion("Usuario " + usuarioLogeado.usuario + " logeado!","linear-gradient(to right, #00b09b, #96c93d)"); 
            }
        }
        
        // Se eliminan los siguientes objetos del localStorage
        localStorage.removeItem('usuarioLogeado');

    } else {
        // Se elimina el objeto usuario en caso de estar en el login
        sessionStorage.removeItem('usuario');
    }
});

// Variables globales
var modalLoading = null;

// Funcion que inserta el html de los modales en el body y activa el modal del loading
function CrearModales() {
    const modalDiv = document.createElement('div');
    modalDiv.innerHTML = `
        <div class="modal fade" id="modalLoading" tabindex="-1" aria-labelledby="modalLoading" aria-hidden="true" data-bs-backdrop="static">
            <div class="modal-dialog modal-ls">
                <div class="modal-content">
                    <div class="modal-body text-center">
                        <div class="row">
                            <div class="col-12">
                                <div class="spinner-border m-5" style="width: 3rem; height: 3rem;" role="status">
                                    <span class="visually-hidden">Cargando...</span>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-12">
                                <label>Cargando...</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>`;
    document.body.appendChild(modalDiv);
    modalLoading = new bootstrap.Modal(document.getElementById('modalLoading'));
}

// Funcion que abre o cierra el modal del loading
function Loading(bandera){
    return new Promise((resolve) => {
        const elementoModal = document.getElementById('modalLoading');
        elementoModal.addEventListener(bandera ? 'shown.bs.modal' : 'hidden.bs.modal', () => {
            resolve();
        }, { once: true });
        if(bandera)
            modalLoading.show();
        else
            modalLoading.hide();
    });
}

// Funcion para consultar a los archivos php
// tabla: el nombre de la tabla, que es el mismo que el archivo php respectivo
// metodo: es el metodo por el cual se va a consultar 
// datos: son los datos que se van a enviar a la consulta
async function consultar(tabla,metodo,datos) {
    debugger
    try {    
        // Se crea la url y se consulta con fetch
        let url = 'http://localhost:8000/api/v1/' + tabla
        const response = await fetch(url, metodo.toUpperCase() !== 'GET' ? 
            {
                method: metodo.toUpperCase(),
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(datos)
            } : 
            {
                method: 'GET'
            } 
        );
        debugger
        return await response.json();
    } catch (error) {
        debugger
        console.error('Error:', error);
    }
}

// Muestra notificaciones
//texto: es el texto que se vera en la notificacion
//color: es el color que tendra la notificacion
function mostrarNotificacion(texto,color) {
    var notificacion = Toastify({
      text: texto,
      duration: 3000,
      gravity: "top-right",
      close: true,
      backgroundColor: color
    });
  
    notificacion.showToast();
}

// Funcion que da un formato de DD-MM-YYYY a las fechas
//fechaString: es el string que contiene la fecha
function formatoFechaString(fechaString) {
    // Crea un objeto Date a partir de la cadena de fecha
    const date = new Date(fechaString);
    
    if (isNaN(date.getTime())) {
        return "Fecha no válida"; // Maneja casos en los que la cadena de fecha no es válida
    }
    
    const day = String(date.getDate()).padStart(2, '0'); // Obtener el día y agregar ceros a la izquierda si es necesario
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Obtener el mes (los meses comienzan desde 0) y agregar ceros a la izquierda si es necesario
    const year = date.getFullYear(); // Obtener el año

    return `${day}-${month}-${year}`;
}

// Funcion que da un formato de dos decimales a los numeros
//fechaString: es el string que contiene la fecha
function formatoDecimalString(valor) {

    let decimal = 0;

    // Se verifica si no es NaN, si es string o si es un numero para su respectiva accion
    if(isNaN(valor)){
        decimal = 0
    }else if(typeof valor === 'string'){
        if(valor === ''){
            decimal = 0
        }else{
            decimal = parseFloat(valor.replace(',', '.'));
        }
    }else{
        decimal = valor
    }

    if (decimal % 1 !== 0) {
        // Si tiene decimales, mostrar dos decimales
        return decimal.toFixed(2);
    } else {
        // Si no tiene decimales, mostrar sin decimales
        return decimal.toString();
    }
}

// Funcion que sirve para cargar los select
// tabla: el nombre de la tabla, que es el mismo que el archivo php respectivo
// idSelect: el id del select que se quiere llenar
// error: mensaje personalizado en caso de que ocurra un error
// datos: datos para llenar el select, son opcionales si se envian no se consulta la base de datos
async function ObtenerSelect(tabla, idSelect, error, datos) {
	try{

        // Se obtiene el select y se limpia
        let select = document.getElementById(idSelect);
        select.innerHTML = ""

        // Se verifica si se enviaron los datos, en caso de que no se consulta la base de datos
        if(typeof datos !== 'undefined' && datos !== null){
            datos.forEach(s => {
                // Creamos una opción para cada select
                let option = document.createElement("option");
                option.value = s.id;
                option.textContent = s.nombre;
                select.appendChild(option);
            });
        }else{
            let data = await consultar(tabla, 'GET', {});
            if(data !== null && typeof data !== 'undefined'){
                data.forEach(s => {
                    // Creamos una opción para cada select
                    let option = document.createElement("option");
                    option.value = s.id;
                    option.textContent = s.nombre;
                    select.appendChild(option);
                });
            }else{
                mostrarNotificacion("No se encontro ningun " + error,"#FF0000") 
            }
        }
	}catch(e){
		mostrarNotificacion("Error: " + e,"#FF0000")  
		console.error('Error:', e);
	}
}

// Funcion que carga el navbar
// pagina: es la pagina actual, sirve para colocar como activo en el navbar
function CargarNavbar(pagina){
    document.getElementById("navbar").innerHTML = `
                    <div  class="container-fluid">
                        <div class="navbar-brand">Comercializadora</div>
                            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                                <span class="navbar-toggler-icon"></span>
                            </button>
                            <div class="collapse navbar-collapse" id="navbarNav">
                                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                                    <li class="nav-item">
                                        <a class="nav-link ${pagina.indexOf('index.html') !== -1 ? 'active' : ''}" href="index.html">Inicio</a>
                                    </li>
                                </ul>
                                <a type="button" class="btn btn-dark" href="login.html">Cerrar Sesion</a>
                            </div>
                    </div>`;
}

