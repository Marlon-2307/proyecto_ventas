"""Entrenamiento de un modelo de regresión simple para predecir 'Sales'.
- Lee data/ventas_clean.csv
- Selecciona variables numéricas y algunas categóricas
- Imputa valores faltantes, escala numéricas y codifica categóricas
- Entrena un modelo de regresión lineal
- Guarda el modelo en models/modelo_regresion.pkl
"""

import pandas as pd
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib

# ============================================================
# RUTAS
# ============================================================
BASE = os.path.join(os.path.dirname(__file__), '..')
IN_PATH = os.path.join(BASE, 'data', 'ventas_clean.csv')
MODEL_PATH = os.path.join(BASE, 'models', 'modelo_regresion.pkl')
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================
def main():
    print('Leyendo dataset procesado:', IN_PATH)
    df = pd.read_csv(IN_PATH, low_memory=False)
    print('Dimensiones:', df.shape)

    # Definir variable objetivo
    if 'Sales' not in df.columns:
        raise SystemExit('El dataset no contiene la columna "Sales".')

    # Selección de columnas
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    num_cols = [c for c in num_cols if c != 'Sales']

    cat_cols = [c for c in df.select_dtypes(include=['object']).columns.tolist()
                if df[c].nunique() < 50]

    features = num_cols + cat_cols
    if not features:
        raise SystemExit('No hay features disponibles. Revisa tu dataset.')

    X = df[features].copy()
    y = pd.to_numeric(df['Sales'], errors='coerce')

    mask = ~y.isna()
    X = X.loc[mask]
    y = y.loc[mask]

    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ========================================================
    # PREPROCESAMIENTO (con Imputer + Encoder + Escalado)
    # ========================================================

    # Pipeline para numéricas
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Pipeline para categóricas
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # Preprocesador completo
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_cols),
            ('cat', categorical_transformer, cat_cols)
        ]
    )

    # Modelo completo
    model = Pipeline(steps=[
        ('pre', preprocessor),
        ('reg', LinearRegression())
    ])

    print('Entrenando modelo...')
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

    # Métricas
    r2 = r2_score(y_test, preds)
    mae = mean_absolute_error(y_test, preds)
    mse = mean_squared_error(y_test, preds)

    print(f'R2: {r2:.4f} | MAE: {mae:.4f} | MSE: {mse:.4f}')

    # Guardar modelo
    joblib.dump(model, MODEL_PATH)
    print('Modelo guardado en:', MODEL_PATH)


if __name__ == '__main__':
    main()
