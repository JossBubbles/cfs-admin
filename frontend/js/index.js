async function iniciarSesion(usuario, password) {
  try {
    const respuesta = await fetch('https://api.ejemplo.com/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ user: usuario, pass: password })
    });

    if (!respuesta.ok) {
      const errorData = await respuesta.json();
      throw new Error(errorData.mensaje || 'Credenciales incorrectas');
    }

    const resultado = await respuesta.json();
    console.log('Autenticación exitosa, Token:', resultado.token);
    return resultado;
    
  } catch (error) {
    console.error('Error en el inicio de sesión:', error.message);
    throw error;
  }
}


(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const user = $('user');
  const pass = $('pass');
  const btn = $('btn');
  const status = $('status');
  const toggleBtn = $('toggle');
  const form = $('form');

  toggleBtn.addEventListener('click', function () {
    const show = pass.type === 'password';
    pass.type = show ? 'text' : 'password';
    this.textContent = show ? 'Ocultar' : 'Mostrar';
    this.setAttribute('aria-pressed', show);
  });


  const check = (fid, mid, hasError, errorMessage) => {
    $(fid).classList.toggle('err', hasError);
    $(mid).textContent = hasError ? errorMessage : '';
    return !hasError;
  };

  // 4. Manejo del evento de envío del formulario
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    status.className = 'msg';
    status.textContent = '';

    const isUserValid = check('f-user', 'm-user', !user.value.trim(), 'Escribe tu usuario.');
    const isPassValid = check('f-pass', 'm-pass', !pass.value, 'Escribe tu contraseña.');

    if (!isUserValid) {
      user.focus();
      return;
    }
    
    if (!isPassValid) {
      pass.focus();
      return;
    }

    btn.disabled = true;
    btn.textContent = 'Ingresando…';

    // Simulación de petición al servidor (reemplazar con llamada fetch real)
    setTimeout(() => {
      btn.disabled = false;
      btn.textContent = 'Ingresar';
      status.className = 'msg ok';
      status.textContent = 'Sesión iniciada. Redirigiendo al panel…';
    }, 1000);
  });
})();