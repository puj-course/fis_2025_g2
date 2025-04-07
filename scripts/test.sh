#!/bin/bash
echo "[TEST] Verificando ejecución del scraper..."

python3 scripts/scraper.py

if [ $? -eq 0 ]; then
    echo "[TEST] El script se ejecutó correctamente."
else
    echo "[TEST] Falló la ejecución del scraper."
    exit 1
fi
