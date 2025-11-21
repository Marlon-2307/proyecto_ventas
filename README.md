# Proyecto: Análisis y Predicción de Ventas con Python y Streamlit

## Estructura del proyecto

proyecto_ventas/
├── data/ventas.csv                # dataset (Sample - Superstore u otro)
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
1. -`data/ventas.csv`.
2. -`pip install -r requirements.txt`
3. Ejecutar scripts: 
   - `python scripts/data_prep.py`
   - `python scripts/eda.py`
   - `python scripts/train_model.py`
4. - `streamlit run app/app.py`

## Notas
- Todos los scripts están comentados
- `scripts/data_prep.py`.
- Trabajo realizado por los estudiantes: Marlon Colon, Johan de Leon 