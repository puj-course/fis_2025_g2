#!/bin/bash
echo "[DEPLOY] Moviendo Excel a carpeta de salida..."

mkdir -p output
mv canasta_familiar_precios.xlsx output/

echo "[DEPLOY] Guardado en output/canasta_familiar_precios.xlsx"
