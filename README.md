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
# Despliegue
![Diagrama de Despliegue](docs/Diagramas/Diagrama%20de%20despliegue.png)
# Componentes
![Diagrama de Componentes](docs/Diagramas/Diagrama%20de%20componentes.png)
# Clases
![Diagrama de Clases](docs/Diagramas/Diagrama%20de%20clases.png)
# EBC
![Diagrama EBC](docs/Diagramas/Diagarma%20EBC.png)


---

## 📁 Estructura del Proyecto

.
├── .github/workflows/ # Pipelines CI/CD

│ ├── Pipeline-PaginaWeb.yml

│ └── scraper-pipeline.yml

├── conf/ # Configuraciones personalizadas
│ └── api/

├── docs/ # Documentación y recursos visuales

│ ├── architecture/

│ │ ├── Diagramas (png/pdf)

│ ├── Datos_Dane/

│ ├── user_guide/, Requisitos, Seguridad, etc.

│ └── Base de Datos.pdf

├── jupyter/ # Notebooks exploratorios

│ ├── datasets/

│ └── notebooks/

├── scripts/ # Scripts CLI y de automatización

│ ├── deploy.sh

│ ├── setup.sh

│ ├── scraper.py

│ ├── pruebas.py

│ └── test.sh

├── src/
│ ├── AI/ # Lógica de predicción ML

│ ├── main/ # Inicializadores generales

│ └── paginaweb/ # Aplicación web completa

│ ├── Backend/ # FastAPI, Telegram, IA en Python

│ ├── Dockerfile.frontend

│ └── Frontend en React (Vite)

├── test/ # Pruebas de unidad e integración

│ ├── test_example.py

│ ├── server.test.js

│ └── archivos de prueba (Excel)

├── docker-compose.yml # Orquestación de servicios

├── requirements.txt # Dependencias Python

├── Makefile # Atajos para tareas comunes

├── README.md

├── LICENSE

└── CONTRIBUTING.md


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


