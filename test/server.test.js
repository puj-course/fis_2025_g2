// tests/server.test.js

/**
 * Este archivo contiene tests de integración para las rutas /login y /register
en el servidor Express definido en backend/server.js.
 * Usa Jest y Supertest.
 *
 * NOTA: Para que Supertest pueda arrancar/cerrar el servidor automáticamente,
 * modifica al final de backend/server.js:
 *
 *   const server = app.listen(3001, () => console.log("Servidor en http://localhost:3001"));
 *   module.exports = server;
 *
 * Así, al hacer `require('../backend/server')`, obtendrás el objeto server
y no sólo el módulo vacío.
 */

const request = require('supertest');
const auth = require('../backend/authService');

// Tomamos el servidor exportado por server.js
let server;

describe('Rutas de autenticación', () => {
  beforeAll(() => {
    // Arranca el servidor
    server = require('../backend/server');
  });

  afterAll((done) => {
    // Cierra el servidor para liberar el puerto
    server.close(done);
  });

  beforeEach(() => {
    // Restablece mocks antes de cada test
    jest.resetAllMocks();
  });

  describe('POST /login', () => {
    test('debe retornar 200 y objeto user en credenciales válidas', async () => {
      // Simula auth.login exitoso
      const usuarioSimulado = { id: 1, nombre: 'juan' };
      auth.login = jest.fn().mockReturnValue(usuarioSimulado);

      const res = await request(server)
        .post('/login')
        .send({ nombreUsuario: 'juan', contrasena: 'secreto' });

      expect(res.status).toBe(200);
      expect(res.body).toEqual({ success: true, user: usuarioSimulado });
      expect(auth.login).toHaveBeenCalledWith('juan', 'secreto');
    });

    test('debe retornar 401 en credenciales inválidas', async () => {
      auth.login = jest.fn().mockReturnValue(null);

      const res = await request(server)
        .post('/login')
        .send({ nombreUsuario: 'juan', contrasena: 'mal' });

      expect(res.status).toBe(401);
      expect(res.body).toEqual({ success: false, message: 'Credenciales inválidas' });
      expect(auth.login).toHaveBeenCalledWith('juan', 'mal');
    });
  });

  describe('POST /register', () => {
    test('debe retornar 200 y mensaje de éxito si se crea usuario', async () => {
      auth.register = jest.fn().mockReturnValue(true);

      const res = await request(server)
        .post('/register')
        .send({ nombreUsuario: 'maria', contrasena: 'clave' });

      expect(res.status).toBe(200);
      expect(res.body).toEqual({ success: true, message: 'Usuario creado exitosamente' });
      expect(auth.register).toHaveBeenCalledWith('maria', 'clave');
    });

    test('debe retornar 400 si el usuario ya existe', async () => {
      auth.register = jest.fn().mockReturnValue(false);

      const res = await request(server)
        .post('/register')
        .send({ nombreUsuario: 'maria', contrasena: 'clave' });

      expect(res.status).toBe(400);
      expect(res.body).toEqual({ success: false, message: 'El usuario ya existe' });
      expect(auth.register).toHaveBeenCalledWith('maria', 'clave');
    });
  });
});
