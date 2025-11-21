"""Limpieza y preparación de datos para el proyecto de ventas.
- Lee data/ventas.csv
- Limpia nulos y duplicados
- Crea columnas útiles: 'Year', 'Month', 'Revenue' (si aplica)
- Guarda dataset procesado en data/ventas_clean.csv
"""
import pandas as pd
import os

IN_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ventas.csv')
OUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ventas_clean.csv')

def main():
    print('Leyendo dataset desde:', IN_PATH)
    df = pd.read_csv(IN_PATH, parse_dates=True, dayfirst=True, low_memory=False)
    print(f'Dimensiones iniciales: {df.shape}')

    # --- Ejemplos de limpieza (ajusta según tu dataset) ---
    # Eliminar duplicados
    df = df.drop_duplicates()

    # Quitar filas con todas las columnas nulas
    df = df.dropna(how='all')

    # Rellenar o eliminar nulos según columna
    # Si existe columna 'Sales' y 'Quantity' se puede crear 'Revenue' si aplica
    if 'Sales' in df.columns and 'Quantity' in df.columns:
        # Convertir a numérico por si hay strings con símbolos
        df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

    # Fecha: intentar detectar columnas que representen fecha
    date_cols = [c for c in df.columns if 'date' in c.lower() or 'fecha' in c.lower()]
    if date_cols:
        for c in date_cols:
            try:
                df[c] = pd.to_datetime(df[c], errors='coerce', dayfirst=True)
            except Exception as e:
                print('No se pudo parsear columna fecha', c, e)

        # Crear columnas Year/Month si hay fecha
        df['Year'] = df[date_cols[0]].dt.year
        df['Month'] = df[date_cols[0]].dt.month

    # Guardar resultado
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    df.to_csv(OUT_PATH, index=False)
    print('Dataset procesado guardado en:', OUT_PATH)
    print('Dimensiones finales:', df.shape)

if __name__ == '__main__':
    main()
