.PHONY: test build up down logs clean

test:
	@echo "🧪 Ejecutando pruebas del backend..."
	cd src/paginaweb/Backend && \
	pip install -r requirements.txt && \
	pytest tests/

build:
	@echo "🐳 Construyendo imágenes Docker..."
	docker build -f src/paginaweb/Backend/Dockerfile.backend -t backend-dev .
	docker build -f src/paginaweb/Dockerfile.frontend -t frontend-dev .

up:
	@echo "🚀 Levantando servicios..."
	docker-compose up -d

down:
	@echo "🛑 Apagando servicios..."
	docker-compose down

logs:
	@echo "📋 Logs del backend:"
	docker logs backend || true
	@echo "📋 Logs del frontend:"
	docker logs frontend || true

clean:
	@echo "🧹 Limpiando imágenes y contenedores..."
	docker-compose down --rmi all --volumes --remove-orphans
