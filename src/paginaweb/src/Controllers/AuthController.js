
import { AuthService } from "../Services/AuthService";

export const AuthController = {
  iniciarSesion(nombreUsuario, contrasena) {
    const usuario = AuthService.login(nombreUsuario, contrasena);
    if (usuario) {
      // Aquí podrías guardar sesión o token (en localStorage por ahora)
      localStorage.setItem("usuario", JSON.stringify(usuario));
      return { exito: true, usuario };
    } else {
      return { exito: false, mensaje: "Credenciales incorrectas" };
    }
  },
};