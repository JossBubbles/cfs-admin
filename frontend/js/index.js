
import { urlserver } from "./cons.js";

"use strict";

// Referencias a los elementos HTML
const $ = (id) => document.getElementById(id);

const form = $("form");
const user = $("user");
const pass = $("pass");
const btn = $("btn");
const status = $("status");
const toggleBtn = $("toggle");

// Comprobar que los elementos necesarios existen
if (!form || !user || !pass || !btn || !status || !toggleBtn) {
  throw new Error(
    "No se encontraron todos los elementos necesarios del formulario."
  );
}

// Mostrar u ocultar la contraseña
toggleBtn.addEventListener("click", function () {
  const show = pass.type === "password";

  pass.type = show ? "text" : "password";
  this.textContent = show ? "Ocultar" : "Mostrar";
  this.setAttribute("aria-pressed", String(show));
});

// Validar campos del formulario
const check = (fid, mid, hasError, errorMessage) => {
  const field = $(fid);
  const message = $(mid);

  field.classList.toggle("err", hasError);
  message.textContent = hasError ? errorMessage : "";

  return !hasError;
};

// Enviar las credenciales al backend
async function iniciarSesion(username, password) {
  const respuesta = await fetch(`${urlserver}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify({
      username,
      password
    })
  });

  // Leer la respuesta del servidor
  const resultado = await respuesta.json();

  if (!respuesta.ok) {
    throw new Error(
      resultado.detail ||
      resultado.mensaje ||
      "Error al iniciar sesión."
    );
  }

  return resultado;
}

// Manejar el envío del formulario
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Limpiar mensajes anteriores
  status.className = "msg";
  status.textContent = "";

  // Validar usuario
  const isUserValid = check(
    "f-user",
    "m-user",
    !user.value.trim(),
    "Escribe tu usuario."
  );

  // Validar contraseña
  const isPassValid = check(
    "f-pass",
    "m-pass",
    !pass.value,
    "Escribe tu contraseña."
  );

  if (!isUserValid) {
    user.focus();
    return;
  }

  if (!isPassValid) {
    pass.focus();
    return;
  }

  // Deshabilitar el botón durante la petición
  btn.disabled = true;
  btn.textContent = "Ingresando…";

  try {
    const resultado = await iniciarSesion(
      user.value.trim(),
      pass.value
    );

    console.log("Respuesta del servidor:", resultado);

    if (!resultado.ok || !resultado.token) {
      throw new Error("El servidor no confirmó el inicio de sesión.");
    }

    // Guardar el token para utilizarlo en futuras peticiones.
    // Esto es una implementación básica; para producción,
    // considera una cookie HttpOnly y Secure.
    sessionStorage.setItem("token", resultado.token);

    status.className = "msg ok";
    status.textContent = "Sesión iniciada correctamente.";

    // Redirigir al panel
    window.location.href = "/panel";

  } catch (error) {
    console.error("Error en el inicio de sesión:", error);

    status.className = "msg error";
    status.textContent =
      error instanceof TypeError
        ? "No se pudo conectar con el servidor. Comprueba la conexión."
        : error.message || "No se pudo iniciar sesión.";

  } finally {
    btn.disabled = false;
    btn.textContent = "Ingresar";
  }
});
