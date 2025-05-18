// tests/server.test.js
const request = require('supertest');
const { Server } = require('../backend/server');
const auth = require('../backend/authService');
const { sendTelegramMessage } = require('../backend/telegramNotifier');

// Mock de módulos
jest.mock('../backend/authService');
jest.mock('../backend/telegramNotifier');

describe('Servidor Express', () => {
  let serverInstance;
  let testApp;

  beforeAll(async () => {
    serverInstance = new Server();
    testApp = serverInstance.start(0); // Puerto aleatorio para pruebas
  });

  afterAll(async () => {
    serverInstance.stop();
  });

  beforeEach(() => {
    jest.clearAllMocks();
  });

  // ================== PRUEBAS LOGIN ==================
  describe('POST /login', () => {
    test('Login exitoso con notificación', async () => {
      auth.login.mockImplementation((user, pass) => ({
        username: 'testuser',
        email: 'test@correo.com',
        phone: '3001234567',
        password: 'secret',
        isPremium: true
      }));

      const res = await request(testApp)
        .post('/login')
        .send({ username: 'testuser', password: 'secret' });

      expect(res.status).toBe(200);
      expect(res.body).toEqual({
        success: true,
        user: {
          username: 'testuser',
          email: 'test@correo.com',
          phone: '3001234567',
          isPremium: true
        }
      });
      expect(sendTelegramMessage).toHaveBeenCalledWith(
        '🔐 Login exitoso:\n• Usuario: testuser'
      );
    });

    test('Login fallido por credenciales incorrectas', async () => {
      auth.login.mockReturnValue(null);

      const res = await request(testApp)
        .post('/login')
        .send({ username: 'fake', password: 'wrong' });

      expect(res.status).toBe(401);
      expect(res.body).toEqual({
        success: false,
        message: "Credenciales inválidas"
      });
    });
  });

  // ================== PRUEBAS REGISTRO ==================
  describe('POST /register', () => {
    test('Registro exitoso con datos completos', async () => {
      auth.register.mockReturnValue(true);

      const userData = {
        username: 'nuevousuario',
        email: 'nuevo@correo.com',
        phone: '3107654321',
        password: 'nuevacontra',
        isPremium: false
      };

      const res = await request(testApp)
        .post('/register')
        .send(userData);

      expect(res.status).toBe(200);
      expect(res.body).toEqual({
        success: true,
        message: "Usuario creado exitosamente"
      });
      expect(sendTelegramMessage).toHaveBeenCalledWith(
        '🆕 Nuevo registro:\n• Usuario: nuevousuario\n• Email: nuevo@correo.com\n• Teléfono: 3107654321\n• Premium: false'
      );
    });

    test('Registro fallido por usuario existente', async () => {
      auth.register.mockReturnValue(false);

      const res = await request(testApp)
        .post('/register')
        .send({
          username: 'existente',
          email: 'existente@correo.com',
          phone: '3209876543',
          password: 'existente',
          isPremium: true
        });

      expect(res.status).toBe(400);
      expect(res.body).toEqual({
        success: false,
        message: "El usuario ya existe"
      });
    });
  });

  // ================== PRUEBAS ADICIONALES ==================
  test('Ruta inexistente devuelve 404', async () => {
    const res = await request(testApp).get('/ruta-inexistente');
    expect(res.status).toBe(404);
  });
});