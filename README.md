# Proyecto: Análisis y Predicción de Ventas con Python y Streamlit

## Estructura del proyecto

proyecto_ventas/
├── data/ventas.csv                # Coloca aquí tu dataset (Sample - Superstore u otro)
├── notebooks/                     # Notebooks o scripts exploratorios
│   └── analisis_exploratorio.py
├── models/
│   └── modelo_regresion.pkl       # Modelo entrenado (generado por train_model.py)
├── app/
│   └── app.py                     # App Streamlit
├── scripts/
│   ├── data_prep.py               # Limpieza y preparación de datos
│   ├── eda.py                     # Gráficos y EDA
│   └── train_model.py             # Entrenamiento y evaluación del modelo
├── requirements.txt
└── TUTORIAL.md                    # Tutorial detallado para el PDF final

## Resumen rápido de cómo usar
1. Coloca tu dataset en `data/ventas.csv`.
2. Instala dependencias: `pip install -r requirements.txt`
3. Ejecuta scripts en orden (opcional): 
   - `python scripts/data_prep.py`
   - `python scripts/eda.py`
   - `python scripts/train_model.py`
4. Inicia la app: `streamlit run app/app.py`

## Notas
- Todos los scripts están comentados y listos para ejecutarse con un dataset de ventas típico.
- Si tu dataset tiene nombres de columnas diferentes, adapta los nombres en `scripts/data_prep.py`.
