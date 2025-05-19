# fis_2025_g2
fis_2025_g2

# 🧠 Plataforma de Predicción de Precios y Notificación Automática (FEED-Back)

Proyecto web completo que permite predecir precios de productos y enviar notificaciones automáticas. Integra:

- Backend en **Python (FastAPI)** y **Node.js**
- Frontend en **React + Vite**
- Contenedores con **Docker y Docker Compose**
- Automatización con **CI/CD usando GitHub Actions**

---
# Diagramas

![Diagrama de Despliegue](docs/Diagramas/Diagrama%20de%20despliegue.png)
![Diagrama de Componentes](docs/Diagramas/Diagrama%20de%20componentes.png)
![Diagrama de Clases](docs/Diagramas/Diagrama%20de%20clases.png)
![Diagrama EBC](docs/Diagramas/Diagarma%20EBC.png)


---

## 📁 Estructura del Proyecto

src/ 

├── paginaweb/

│ ├── Backend/

│ │ ├── IA.py # Predicción con modelos de ML

│ │ ├── notify.py # Envío de notificaciones (Telegram, etc.)

│ │ ├── server.js # API Node.js / Interfaz con frontend

│ │ └── requirements.txt

│ ├── Components/ # Componentes React

│ ├── Controllers/ # Lógica de control del frontend

│ ├── Models/ # Modelos de datos JS

│ ├── Routers/ # Rutas JS

│ ├── Services/ # Servicios (API calls, etc.)

│ ├── views/ # Vistas de la aplicación

│ ├── App.jsx

│ ├── main.jsx

│ ├── index.css

│ └── Dockerfile.frontend

├── tests/ # Pruebas backend y frontend

├── Dockerfile.backend

├── docker-compose.yml

└── .github/

└── workflows/

└── ci.yml # Pipeline CI/CD


---

## ⚙️ Requisitos

- Docker
- Docker Compose
- (Opcional) Node.js y Python si se desea ejecutar localmente sin contenedores

⚙️ CI/CD con GitHub Actions
Este repositorio cuenta con un pipeline automatizado definido en .github/workflows/ci.yml. El flujo CI/CD ejecuta:

✅ Pruebas Backend: Ejecuta pytest sobre src/paginaweb/tests

✅ Pruebas Frontend: Corre npm test tras npm ci

🐳 Build de imágenes Docker: Solo si todas las pruebas anteriores son exitosas

Desencadenadores
El pipeline se ejecuta automáticamente en:

Push a cualquier rama que modifique archivos en src/

Pull requests que incluyan cambios en src/

🧠 Funcionalidades
🔍 Predicción de precios usando modelos de ML

📩 Notificaciones automáticas (Telegram)

🖥️ Interfaz interactiva desarrollada con React

⚙️ Automatización de pruebas y builds con GitHub Actions

🐳 Contenedores portables con Docker


# Desarrollo y entrenamiento de IA:

  - Lenguaje de programacion: Python (.py)
  
  - Modelo: Regresión multivariable (MLR, mas info en: https://www.ugr.es/~montero/matematicas/regresion_lineal.pdf     ----     https://seh-lelha.org/construccion-modelos-regresion-    multivariantes/)
  
  - Datos: Recoleccion manual para mercados locales, uso de barridos (Sweeps) para recopliacion de informacion de cadenas e historicos de precios nacionales.

  -Uso de algoritmo de scraping web en Python por medio de Selenium y BeautifulSoup4 (Olimpica, Jumbo, Exito, etc.).


Puedes encontrar mas informacion al respecto en nuestra Wiki: https://github.com/puj-course/fis_2025_g2/wiki/FeedBack-Home-Wiki


