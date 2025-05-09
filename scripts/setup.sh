#!/bin/bash
echo "[SETUP] Instalando dependencias del proyecto..."

python3 -m pip install --upgrade pip
pip install -r requirements.txt

mkdir -p temp

echo "[SETUP] Listo."
