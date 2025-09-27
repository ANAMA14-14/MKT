# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 07:45:45 2025
@author: anama
"""

import streamlit as st
import pandas as pd
import altair as alt

# ======================
# 1. Configuración inicial
# ======================
st.set_page_config(page_title="📊 Storytelling de Ventas", layout="wide")
st.title("📊 Storytelling de Ventas por País y Categoría")
st.markdown("Este dashboard analiza automáticamente las ventas y descuentos por país y categoría usando datos desde GitHub.")

# ======================
# 2. Cargar datos desde GitHub
# ======================
github_csv_url = "https://github.com/ANAMA14-14/MKT/main/superstore.csv"

try:
    df = pd.read_csv(github_csv_url)
    st.success("✅ Datos cargados correctamente desde GitHub.")
except Exception as e:
    st.error(f"❌ Error al cargar el archivo desde GitHub: {e}")
    st.stop()

# ======================
# 3. Validación de columnas esperadas
# ======================
required_cols = ["Country", "Category", "Sales", "Discount"]
missing = [col for col in required_cols if col not in df.columns]
if missing:
    st.error(f"❌ Faltan las siguientes columnas en el dataset: {missing}")
    st.stop()

# ======================
# 4. Filtros interactivos
# ======================
st.sidebar.header("🔍 Filtros")

# Filtro por país
countries = df["Country"].unique().tolist()
selected_countries = st.sidebar.multiselect("Selecciona País(es)", countries, default=countries[:3])
df = df[df["Country"].isin(selected_countries)]

# Filtro por categoría
categories = df["Category"].unique().tolist()
selected_categories = st.sidebar.multiselect("Selecciona Categoría(s)", categories, default=categories[:2])
df = df[df["Category"].isin(selected_categories)]

# Top N por ventas
top_n = st.sidebar.slider("Top N registros por ventas", min_value=5, max_value=50, value=10)
df = df.sort_values(by="Sales", ascending=False).head(top_n)

# ======================
# 5. Paleta de colores
# ======================
color_scheme = st.sidebar.selectbox("🎨 Paleta de colores", ["category10", "tableau10", "dark2", "set1"])

# ======================
# 6. Storytelling visual
# ======================
st.subheader("📊 Ventas por Categoría")
bar_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("Category:N", sort="-y"),
    y=alt.Y("Sales:Q"),
    color=alt.Color("Category:N", scale=alt.Scale(scheme=color_scheme)),
    tooltip=["Country", "Category", "Sales", "Discount"]
).properties(width=700, height=400)

max_row = df.loc[df["Sales"].idxmax()]
anot_bar = alt.Chart(pd.DataFrame({
    "Category": [max_row["Category"]],
    "Sales": [max_row["Sales"]],
    "label": ["⬆ Mayor venta"]
})).mark_text(dy=-10, color="red", fontWeight="bold").encode(
    x="Category:N", y="Sales:Q", text="label"
)

st.altair_chart(bar_chart + anot_bar, use_container_width=True)

st.subheader("📈 Descuento promedio por país")
discount_chart = alt.Chart(df).mark_bar().encode(
    x=alt.X("Country:N"),
    y=alt.Y("mean(Discount):Q", title="Descuento promedio"),
    color=alt.Color("Country:N", scale=alt.Scale(scheme=color_scheme)),
    tooltip=["Country", "mean(Discount)"]
).properties(width=700, height=400)

st.altair_chart(discount_chart, use_container_width=True)

st.subheader("🔀 Relación entre Ventas y Descuento")
scatter_chart = alt.Chart(df).mark_circle(size=80).encode(
    x=alt.X("Discount:Q", scale=alt.Scale(zero=False)),
    y=alt.Y("Sales:Q", scale=alt.Scale(zero=False)),
    color=alt.Color("Category:N", scale=alt.Scale(scheme=color_scheme)),
    tooltip=["Country", "Category", "Sales", "Discount"]
).properties(width=700, height=400)

st.altair_chart(scatter_chart, use_container_width=True)

# ======================
# 7. Insights narrativos
# ======================
st.subheader("🧠 Insights clave")

top_country = df.groupby("Country")["Sales"].sum().idxmax()
top_category = df.groupby("Category")["Sales"].sum().idxmax()
max_discount = df.loc[df["Discount"].idxmax()]

st.markdown(f"""
- 🌍 El país con mayores ventas es **{top_country}**.
- 🏷️ La categoría más vendida es **{top_category}**.
- 💸 El mayor descuento registrado fue de **{max_discount['Discount']}%** en **{max_discount['Category']}** ({max_discount['Country']}).
""")
    
    
# =======================================================================
# cd  "C:\Users\anama\Downloads"
# streamlit run Storytelling.py
