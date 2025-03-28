#!/bin/bash

BASE_DIR="/Users/martinagarciagonzalez/gd_clv-14/etl"  # Ruta correcta de la carpeta ETL

# Registrar la ejecución
echo "Ejecución iniciada: $(date)" >> "$BASE_DIR/log_etl.txt"

# Ejecutar cada notebook con Papermill
papermill "$BASE_DIR/01_modelo_dimensional.ipynb" "$BASE_DIR/01_modelo_dimensional_output.ipynb"
papermill "$BASE_DIR/02_vision_cliente.ipynb" "$BASE_DIR/02_vision_cliente_output.ipynb"
papermill "$BASE_DIR/03_regresion_cliente.ipynb" "$BASE_DIR/03_regresion_cliente_output.ipynb"

# Finalizar registro
echo "Ejecución finalizada: $(date)" >> "$BASE_DIR/log_etl.txt"