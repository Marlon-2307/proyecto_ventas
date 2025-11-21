import streamlit as st
import pandas as pd
import os
import joblib

# Config
BASE = os.path.join(os.path.dirname(__file__), '..')
DATA_PATH = os.path.join(BASE, 'data', 'ventas_clean.csv')
MODEL_PATH = os.path.join(BASE, 'models', 'modelo_regresion.pkl')
FIGURES_DIR = os.path.join(BASE, 'output', 'figures')

st.set_page_config(page_title="Análisis y Predicción de Ventas", layout="wide")
st.title("📊 Análisis y Predicción de Ventas")
st.sidebar.header("Controles")

# Cargar modelo
@st.cache_data
def load_model(path):
    if os.path.exists(path):
        return joblib.load(path)
    return None

model = load_model(MODEL_PATH)

# Cargar dataset
@st.cache_data
def load_data(path):
    if os.path.exists(path):
        return pd.read_csv(path, low_memory=False)
    return None

df = load_data(DATA_PATH)

# Dataset
st.header("Vista rápida del dataset")
if df is not None:
    st.dataframe(df.head(200))
else:
    st.warning("No se encontró data/ventas_clean.csv. Ejecuta data_prep.py primero.")

# Resumen
if df is not None:
    st.header("Resumen de estadísticas")
    st.write(df.describe(include='all').T)

# Mostrar figuras del EDA
st.header("📈 Gráficos del EDA")
if os.path.isdir(FIGURES_DIR):
    figs = [f for f in os.listdir(FIGURES_DIR) if f.endswith(('.png','.jpg','.jpeg'))]
    if figs:
        for f in figs:
            st.subheader(f)
            st.image(os.path.join(FIGURES_DIR, f), use_column_width=True)
    else:
        st.info("No se encontraron imágenes. Ejecuta eda.py.")
else:
    st.info("Carpeta output/figures no existe.")

# Predicción
st.header("🔮 Predicción")

if model is None:
    st.warning("No se encontró el modelo entrenado. Ejecuta train_model.py.")
else:
    st.success("Modelo cargado exitosamente.")

    if df is not None:
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        if "Sales" in num_cols:
            num_cols.remove("Sales")
        cat_cols = df.select_dtypes(include=['object']).columns.tolist()
        cat_cols = [c for c in cat_cols if df[c].nunique() < 50]
        features = num_cols + cat_cols
    else:
        features = []

    st.subheader("Predicción individual")
    if features:
        inputs = {}
        with st.form("pred_form"):
            for col in features:
                if col in num_cols:
                    inputs[col] = st.number_input(col, value=0.0)
                else:
                    values = df[col].dropna().unique().tolist()
                    inputs[col] = st.selectbox(col, values)
            sub = st.form_submit_button("Predecir")

        if sub:
            try:
                x_df = pd.DataFrame([inputs])
                pred = model.predict(x_df)[0]
                st.success(f"Predicción de Sales: {pred:.2f}")
            except Exception as e:
                st.error(f"Error: {e}")

    st.subheader("Predicción por archivo CSV")
    up = st.file_uploader("Sube un CSV con las mismas columnas usadas en el entrenamiento", type=["csv"])
    if up is not None:
        df_up = pd.read_csv(up)
        try:
            preds = model.predict(df_up)
            df_up["predicted_Sales"] = preds
            st.dataframe(df_up.head(200))
            st.download_button("Descargar predicciones",
                               df_up.to_csv(index=False).encode("utf-8"),
                               file_name="predicciones.csv")
        except Exception as e:
            st.error(f"Error al predecir: {e}")

# Footer estable sin triple backticks
st.markdown("---")
st.markdown(
    "### Instrucciones rápidas:\n"
    "- Ejecuta los scripts en este orden:\n"
    "  1. python scripts/data_prep.py\n"
    "  2. python scripts/eda.py\n"
    "  3. python scripts/train_model.py\n"
    "- Luego ejecuta la aplicación con:\n"
    "  python -m streamlit run app/app.py\n"
)
