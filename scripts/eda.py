"""Genera gráficas de EDA y guarda algunas figuras en output/figures.
Usa matplotlib y seaborn.
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

BASE = os.path.join(os.path.dirname(__file__), '..')
IN_PATH = os.path.join(BASE, 'data', 'ventas_clean.csv')
OUT_DIR = os.path.join(BASE, 'output', 'figures')
os.makedirs(OUT_DIR, exist_ok=True)

def main():
    print('Leyendo dataset procesado:', IN_PATH)
    df = pd.read_csv(IN_PATH, low_memory=False)
    print('Dimensiones:', df.shape)

    # Ejemplo: ventas por región (si existe columna 'Region' y 'Sales')
    if 'Region' in df.columns and 'Sales' in df.columns:
        agg = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
        plt.figure(figsize=(8,5))
        sns.barplot(x=agg.index, y=agg.values)
        plt.title('Ventas por Región')
        plt.ylabel('Sales')
        plt.tight_layout()
        path = os.path.join(OUT_DIR, 'ventas_por_region.png')
        plt.savefig(path)
        plt.close()
        print('Guardado:', path)

    # Ejemplo: correlación de variables numéricas
    num = df.select_dtypes(include=['number'])
    if not num.empty:
        plt.figure(figsize=(10,8))
        sns.heatmap(num.corr(), annot=True, fmt='.2f', cmap='coolwarm')
        plt.title('Matriz de correlación (numéricas)')
        path = os.path.join(OUT_DIR, 'correlacion_numericas.png')
        plt.savefig(path)
        plt.close()
        print('Guardado:', path)

    # Boxplot ejemplo: Sales por Category
    if 'Category' in df.columns and 'Sales' in df.columns:
        plt.figure(figsize=(10,6))
        sns.boxplot(x='Category', y='Sales', data=df)
        plt.title('Distribución de Sales por Category')
        plt.tight_layout()
        path = os.path.join(OUT_DIR, 'boxplot_sales_category.png')
        plt.savefig(path)
        plt.close()
        print('Guardado:', path)

    print('EDA completado. Revisa la carpeta output/figures')

if __name__ == '__main__':
    main()
