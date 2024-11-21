document.addEventListener('DOMContentLoaded', async function() {
	if (window.location.href.indexOf('login.html') !== -1){
		let usuarioRegistrado = JSON.parse(localStorage.getItem('usuarioRegistrado'))
		if(typeof usuarioRegistrado !== 'undefined' &&  usuarioRegistrado !== null && typeof usuarioRegistrado.usuario !== 'undefined' && usuarioRegistrado.usuario !== null){
			mostrarNotificacion("Usuario " + usuarioRegistrado.usuario + " registrado!","linear-gradient(to right, #00b09b, #96c93d)") 
		}
	}
	localStorage.removeItem('usuarioRegistrado');
	localStorage.removeItem('persona');
});

// Funcion que valida los campos del formulario del login y registro
(function () {
	'use strict'

	// Fetch all the forms we want to apply custom Bootstrap validation styles to
	var forms = document.querySelectorAll('.needs-validation')

	// Loop over them and prevent submission
	Array.prototype.slice.call(forms)
		.forEach(function (form) {
			form.addEventListener('submit', function (event) {
				if (!form.checkValidity()) {
					event.preventDefault()
					event.stopPropagation()
				}

				form.classList.add('was-validated')
			}, false)
		})
})()

// Funcion que verifica si existe el usuario
async function verificarUsuario() {
	try{

		let usuario = document.getElementById("usuario")
		let clave = document.getElementById("clave")

		const objeto = {
			usuario: usuario.value,
			clave: clave.value
		}

		usuario.value = ''
		clave.value = ''

		const datos = await consultar('usuario/AutenticarUsuario', 'POST', objeto); 

		if(typeof datos === 'undefined' || datos === null){
			mostrarNotificacion("No se encontro ningun usuario","#FF0000") 
			return
		}

		// Se crea en el sessionStorage el usuario y se redirige al index
		const usuarioLogeado = {
			id: datos.id,
			usuario: datos.usuario,
			rol: datos.rol,
		}

		sessionStorage.setItem('usuario', JSON.stringify(usuarioLogeado))
		localStorage.setItem('usuarioLogeado', JSON.stringify(usuarioLogeado))
		if(datos.rol.id === 1){
			window.location.href = "tablacitas.html";
		}else{
			window.location.href = "somos.html";
		}
			
		
	}catch(e){
		mostrarNotificacion("Error: " + e,"#FF0000")  
		console.error('Error:', e);
	}
}

// Funcion para crear usuario
async function crearUsuario() {
	try{

		let usuario = document.getElementById("usuario")
		let clave = document.getElementById("clave")
		let repetirClave = document.getElementById("repetirClave")

		if(clave.value !== repetirClave.value){
			mostrarNotificacion("Las contraseñas no coiciden","#FF0000") 
			return;
		}

		let objeto = {
			usuario: usuario.value,
			clave: clave.value,
			rolId: 2
		}

		usuario.value = ''
		clave.value = ''
		repetirClave.value = ''

		let datos = await consultar('usuario/CrearUsuario', 'POST', objeto);

		if(datos === null || typeof datos === 'undefined'){
			mostrarNotificacion("Error al crear el usuario","#FF0000") 
			return
		}

		// Se guarda en el localStorage el objeto usuarioRegistrado y se redirige al login
		let usuarioRegistrado = {
			usuario: datos.usuario
		}
		localStorage.setItem('usuarioRegistrado', JSON.stringify(usuarioRegistrado))
		window.location.href = "login.html";
	}catch(e){
		mostrarNotificacion("Error: " + e,"#FF0000")  
		console.error('Error:', e);
	}
}

