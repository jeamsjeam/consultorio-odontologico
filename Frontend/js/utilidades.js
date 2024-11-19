document.addEventListener("DOMContentLoaded", async function () {

    // Se valida si la ruta no es index, registro o recuperacion
    if (window.location.href.indexOf('login.html') === -1 && 
        window.location.href.indexOf('registro.html') === -1) {

        // Se carga el navbar y se crea el html de los modales
        if(window.location.href.indexOf('tablacitas.html') === -1 && window.location.href.indexOf('pacientes.html') === -1){
            CargarNavbar(window.location.href);
            CargarFooter()
        }
        //CrearModales();

        // Se verifica si existe usuario en el sessionStorage
        //En caso de no existir se redigire al login 
        let datosUsuario = JSON.parse(sessionStorage.getItem('usuario'));
        if (typeof datosUsuario === 'undefined' || datosUsuario === null) {
            window.location.href = "login.html";
        }

        //Se verifica si no ex el index
        if (window.location.href.indexOf('somos.html') !== -1) {

            // Se verifica si existe usarioLogeado, para poder mostrar una notificacion en verde
            let usuarioLogeado = JSON.parse(localStorage.getItem('usuarioLogeado'));
            if (typeof usuarioLogeado !== 'undefined' &&  usuarioLogeado !== null && typeof usuarioLogeado.usuario !== 'undefined' && usuarioLogeado.usuario !== null) {
                mostrarNotificacion("Usuario " + usuarioLogeado.usuario + " logeado!","linear-gradient(to right, #00b09b, #96c93d)"); 
            }
        }
        
        // Se eliminan los siguientes objetos del localStorage
        localStorage.removeItem('usuarioLogeado');

        if((window.location.href.indexOf('tablacitas.html') !== -1 || window.location.href.indexOf('pacientes.html')) !== -1 && datosUsuario.rol.id !== 1){
            window.location.href = "login.html";
        }

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

// Funcion para consultar api rest
// ruta: Ruta del servicio a consultar
// metodo: es el metodo por el cual se va a consultar 
// datos: son los datos que se van a enviar a la consulta
async function consultar(ruta,metodo,datos) {
    try {    
        // Se crea la url y se consulta con fetch
        let url = 'http://127.0.0.1:5000/' + ruta
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
        return await response.json();
    } catch (error) {
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
// ruta: Ruta del servicio
// idSelect: el id del select que se quiere llenar
// error: mensaje personalizado en caso de que ocurra un error
// datos: datos para llenar el select, son opcionales si se envian no se consulta la base de datos
async function ObtenerSelect(ruta, idSelect, error, datos) {
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
            let data = await consultar(ruta, 'GET', null);
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
            <a class="navbar-brand p-1 text-white" href="somos.html" style="background-color: #ba87ca; border-radius: 5px !important;">
                <div class="image-container-navbar">
                    <img src="imagenes/IMG-20240810-WA0005.png" alt="logo">
                </div>
            </a>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item mx-1">
                        <a class="nav-link ${pagina.indexOf('somos.html') !== -1 ? 'active' : ''}" href="somos.html">Quienes somos</a>
                    </li>
                    <li class="nav-item mx-1">
                        <a class="nav-link ${pagina.indexOf('galeria.html') !== -1 ? 'active' : ''}" href="galeria.html">Galeria</a>
                    </li>
                    <li class="nav-item mx-1">
                        <a class="nav-link ${pagina.indexOf('servicios.html') !== -1 ? 'active' : ''}" href="servicios.html">Servicios</a>
                    </li>
                    <li class="nav-item mx-1">
                        <a class="nav-link ${pagina.indexOf('consejos.html') !== -1 ? 'active' : ''}" href="consejos.html">Consejos deltal</a>
                    </li>
                    <li class="nav-item mx-1" style="background-color: #4d0aa7; border-radius: 10px !important;">
                        <a class="nav-link text-white ${pagina.indexOf('citas.html') !== -1 ? 'active' : ''}" href="citas.html">RESERVACION DE CITAS</a>
                    </li>
                </ul>
                <a type="button" class="btn btn-secondary" href="login.html">Cerrar Sesion</a>
            </div>`;
}


function CargarFooter(){
    document.getElementById("footer").innerHTML = ` 
            <div class="col-3 d-flex align-items-center">
                <span class="text-white">&copy; SonR-Isas Clínica Odontológica</span>
            </div>

             <div class="col-7 d-flex align-items-left">
                
                <div class="mb-3 me-2 mb-md-0 text-muted lh-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-crosshair2 text-white" viewBox="0 0 16 16">
                        <path d="M8 0a.5.5 0 0 1 .5.5v.518A7 7 0 0 1 14.982 7.5h.518a.5.5 0 0 1 0 1h-.518A7 7 0 0 1 8.5 14.982v.518a.5.5 0 0 1-1 0v-.518A7 7 0 0 1 1.018 8.5H.5a.5.5 0 0 1 0-1h.518A7 7 0 0 1 7.5 1.018V.5A.5.5 0 0 1 8 0m-.5 2.02A6 6 0 0 0 2.02 7.5h1.005A5 5 0 0 1 7.5 3.025zm1 1.005A5 5 0 0 1 12.975 7.5h1.005A6 6 0 0 0 8.5 2.02zM12.975 8.5A5 5 0 0 1 8.5 12.975v1.005a6 6 0 0 0 5.48-5.48zM7.5 12.975A5 5 0 0 1 3.025 8.5H2.02a6 6 0 0 0 5.48 5.48zM10 8a2 2 0 1 0-4 0 2 2 0 0 0 4 0"/>
                    </svg>
                </div>

                <span class="text-white">Diagonal al grupo Sucre, en dirección hacia la plaza Bolívar, centro de Rubio., Rubio, Venezuela 5030</span>
            </div>
        
            <ul class="nav col-2 justify-content-end list-unstyled d-flex">
                <li class="ms-3">
                    <a class="text-muted" href="https://www.instagram.com/sonr_isas.co/" target="_blank">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-twitter-x text-white" viewBox="0 0 16 16">
                            <path d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865z"/>
                        </svg>
                    </a>
                </li>
                <li class="ms-3">
                    <a class="text-muted" href="https://www.instagram.com/sonr_isas.co/" target="_blank">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-instagram text-white" viewBox="0 0 16 16">
                            <path d="M8 0C5.829 0 5.556.01 4.703.048 3.85.088 3.269.222 2.76.42a3.9 3.9 0 0 0-1.417.923A3.9 3.9 0 0 0 .42 2.76C.222 3.268.087 3.85.048 4.7.01 5.555 0 5.827 0 8.001c0 2.172.01 2.444.048 3.297.04.852.174 1.433.372 1.942.205.526.478.972.923 1.417.444.445.89.719 1.416.923.51.198 1.09.333 1.942.372C5.555 15.99 5.827 16 8 16s2.444-.01 3.298-.048c.851-.04 1.434-.174 1.943-.372a3.9 3.9 0 0 0 1.416-.923c.445-.445.718-.891.923-1.417.197-.509.332-1.09.372-1.942C15.99 10.445 16 10.173 16 8s-.01-2.445-.048-3.299c-.04-.851-.175-1.433-.372-1.941a3.9 3.9 0 0 0-.923-1.417A3.9 3.9 0 0 0 13.24.42c-.51-.198-1.092-.333-1.943-.372C10.443.01 10.172 0 7.998 0zm-.717 1.442h.718c2.136 0 2.389.007 3.232.046.78.035 1.204.166 1.486.275.373.145.64.319.92.599s.453.546.598.92c.11.281.24.705.275 1.485.039.843.047 1.096.047 3.231s-.008 2.389-.047 3.232c-.035.78-.166 1.203-.275 1.485a2.5 2.5 0 0 1-.599.919c-.28.28-.546.453-.92.598-.28.11-.704.24-1.485.276-.843.038-1.096.047-3.232.047s-2.39-.009-3.233-.047c-.78-.036-1.203-.166-1.485-.276a2.5 2.5 0 0 1-.92-.598 2.5 2.5 0 0 1-.6-.92c-.109-.281-.24-.705-.275-1.485-.038-.843-.046-1.096-.046-3.233s.008-2.388.046-3.231c.036-.78.166-1.204.276-1.486.145-.373.319-.64.599-.92s.546-.453.92-.598c.282-.11.705-.24 1.485-.276.738-.034 1.024-.044 2.515-.045zm4.988 1.328a.96.96 0 1 0 0 1.92.96.96 0 0 0 0-1.92m-4.27 1.122a4.109 4.109 0 1 0 0 8.217 4.109 4.109 0 0 0 0-8.217m0 1.441a2.667 2.667 0 1 1 0 5.334 2.667 2.667 0 0 1 0-5.334"/>
                        </svg>
                    </a>
                </li>
                <li class="ms-3">
                    <a class="text-muted" href="https://www.facebook.com/profile.php?id=100063803422805" target="_blank">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-facebook text-white" viewBox="0 0 16 16">
                            <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951"/>
                        </svg>
                    </a>
                </li>
            </ul>`;
}

