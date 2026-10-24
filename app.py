import math
import random
import statistics
from collections import Counter

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Asistente de Estadística Aplicada", page_icon="📊", layout="wide")

st.title("📊 Asistente Virtual de Estadística Aplicada")
st.caption("Universidad Mariano Gálvez de Guatemala | Facultad de Ingeniería")
st.markdown("""
**Integrantes:** Cristopher Cruz y Pablo André  
**Carné:** 2990-24-19768  
**Carrera:** Ingeniería en Sistemas | **Sección:** A
""")
st.divider()

def parse_data(raw):
    raw = raw.replace(";", ",").replace("\n", ",")
    try:
        vals = [float(x.strip()) for x in raw.split(",") if x.strip()]
    except ValueError:
        raise ValueError("Usa únicamente números separados por comas. Ejemplo: 2.1, 2.3, 2.2")
    if not vals:
        raise ValueError("Ingresa al menos un dato.")
    if not all(math.isfinite(x) for x in vals):
        raise ValueError("Los datos deben ser números finitos.")
    return vals

def fmt(x):
    return f"{x:.4f}".rstrip("0").rstrip(".") if isinstance(x, (float, np.floating)) else str(x)

def stats_table(data):
    n = len(data)
    ordered = sorted(data)
    mean = statistics.mean(data)
    median = statistics.median(data)
    counts = Counter(data)
    max_freq = max(counts.values())
    modes = sorted([x for x, c in counts.items() if c == max_freq]) if max_freq > 1 else []
    data_range = max(data) - min(data)
    pop_var = statistics.pvariance(data) if n >= 1 else 0
    pop_std = math.sqrt(pop_var)
    sample_var = statistics.variance(data) if n >= 2 else None
    sample_std = statistics.stdev(data) if n >= 2 else None
    q1, q3 = np.percentile(ordered, [25, 75])
    return {
        "n": n, "ordered": ordered, "mean": mean, "median": median,
        "modes": modes, "range": data_range, "pop_var": pop_var,
        "pop_std": pop_std, "sample_var": sample_var, "sample_std": sample_std,
        "q1": q1, "q3": q3
    }

def show_stats(data, show_steps=True):
    s = stats_table(data)
    st.subheader("Resultados")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Cantidad de datos (n)", s["n"])
    c2.metric("Media", fmt(s["mean"]))
    c3.metric("Mediana", fmt(s["median"]))
    c4.metric("Rango", fmt(s["range"]))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Desv. estándar poblacional", fmt(s["pop_std"]))
    c2.metric("Varianza poblacional", fmt(s["pop_var"]))
    c3.metric("Desv. estándar muestral", fmt(s["sample_std"]) if s["sample_std"] is not None else "Requiere n ≥ 2")
    c4.metric("Varianza muestral", fmt(s["sample_var"]) if s["sample_var"] is not None else "Requiere n ≥ 2")
    if s["modes"]:
        st.write("**Moda(s):** " + ", ".join(fmt(x) for x in s["modes"]))
    else:
        st.write("**Moda:** no hay moda única (ningún valor se repite más que los demás).")
    st.write(f"**Cuartil 1 (Q1):** {fmt(s['q1'])}  |  **Cuartil 3 (Q3):** {fmt(s['q3'])}")
    st.write("**Datos ordenados:** " + ", ".join(fmt(x) for x in s["ordered"]))
    if show_steps:
        st.subheader("Procedimiento y fórmulas")
        st.markdown(f"""
1. **Media:** suma de los datos dividida entre la cantidad de datos.  
   \\(\\bar x = \\frac{{\\sum x_i}}{{n}} = \\frac{{{fmt(sum(data))}}}{{{s['n']}}} = {fmt(s['mean'])}\\)
2. **Mediana:** se ordenan los datos y se obtiene el valor central.  
   Datos ordenados: `{', '.join(fmt(x) for x in s['ordered'])}` → mediana = **{fmt(s['median'])}**.
3. **Rango:** valor máximo menos valor mínimo.  
   \\(R = x_{{max}} - x_{{min}} = {fmt(max(data))} - {fmt(min(data))} = {fmt(s['range'])}\\)
4. **Varianza poblacional:** \\(\\sigma^2 = \\frac{{\\sum (x_i-\\bar x)^2}}{{n}} = {fmt(s['pop_var'])}\\)
5. **Desviación estándar poblacional:** \\(\\sigma = \\sqrt{{\\sigma^2}} = {fmt(s['pop_std'])}\\)
""")
        if s["sample_std"] is not None:
            st.markdown(f"""
6. **Varianza muestral:** \\(s^2 = \\frac{{\\sum (x_i-\\bar x)^2}}{{n-1}} = {fmt(s['sample_var'])}\\)
7. **Desviación estándar muestral:** \\(s = \\sqrt{{s^2}} = {fmt(s['sample_std'])}\\)
""")
        else:
            st.info("Para calcular varianza y desviación estándar muestral se necesitan al menos dos datos.")

tabs = st.tabs(["📈 Estadística descriptiva", "🧪 Datos experimentales", "📊 Frecuencias y gráficas", "🎲 Probabilidad", "📉 Correlación y regresión", "📝 Práctica", "📚 Ejemplos"])

with tabs[0]:
    st.header("Calculadora de estadística descriptiva")
    raw = st.text_area("Ingresa números separados por comas", "2.1, 2.3, 2.2, 2.4, 2.0", key="desc")
    if st.button("Calcular estadísticas", key="calc_desc"):
        try:
            data = parse_data(raw)
            show_stats(data)
            st.success("Interpretación: la media representa el promedio; la desviación estándar indica qué tan dispersos están los datos respecto de la media.")
        except ValueError as e:
            st.error(str(e))

with tabs[1]:
    st.header("Procesamiento de mediciones físicas")
    st.write("Ingresa mediciones y una unidad (por ejemplo, A, V, m, s o kg).")
    raw_exp = st.text_area("Mediciones", "2.1, 2.3, 2.2, 2.4, 2.0", key="exp")
    unit = st.text_input("Unidad", "A")
    if st.button("Analizar mediciones", key="calc_exp"):
        try:
            data = parse_data(raw_exp)
            show_stats(data)
            s = stats_table(data)
            st.info(f"Se analizaron {s['n']} mediciones en {unit or 'unidades no especificadas'}. Promedio: {fmt(s['mean'])} {unit}. Desviación estándar muestral: {fmt(s['sample_std']) if s['sample_std'] is not None else 'no disponible'} {unit}.")
        except ValueError as e:
            st.error(str(e))

with tabs[2]:
    st.header("Tabla de frecuencias e histogramas")
    raw_freq = st.text_area("Datos para la tabla de frecuencias", "1, 2, 2, 3, 3, 3, 4, 4, 5", key="freq")
    if st.button("Crear tabla y gráfica", key="calc_freq"):
        try:
            data = parse_data(raw_freq)
            counts = Counter(data)
            total = len(data)
            df = pd.DataFrame({"Valor": sorted(counts), "Frecuencia absoluta": [counts[x] for x in sorted(counts)]})
            df["Frecuencia relativa"] = df["Frecuencia absoluta"] / total
            df["Frecuencia acumulada"] = df["Frecuencia absoluta"].cumsum()
            st.dataframe(df, use_container_width=True)
            fig, ax = plt.subplots()
            ax.hist(data, bins="auto", edgecolor="black")
            ax.set_title("Histograma")
            ax.set_xlabel("Valor")
            ax.set_ylabel("Frecuencia")
            st.pyplot(fig)
            if len(data) >= 2:
                fig2, ax2 = plt.subplots()
                ax2.scatter(range(1, len(data)+1), data)
                ax2.set_title("Diagrama de dispersión por orden")
                ax2.set_xlabel("Número de observación")
                ax2.set_ylabel("Valor")
                st.pyplot(fig2)
        except ValueError as e:
            st.error(str(e))

with tabs[3]:
    st.header("Probabilidad básica y distribución normal")
    st.subheader("Probabilidad clásica")
    favorable = st.number_input("Resultados favorables", min_value=0, value=2, step=1)
    total = st.number_input("Resultados posibles", min_value=1, value=6, step=1)
    if st.button("Calcular probabilidad"):
        if favorable > total:
            st.error("Los resultados favorables no pueden superar los resultados posibles.")
        else:
            p = favorable / total
            st.write(f"Fórmula: **P(A) = casos favorables / casos posibles**")
            st.write(f"Sustitución: P(A) = {favorable}/{total} = **{p:.4f} ({p*100:.2f}%)**")
    st.subheader("Distribución normal")
    col1, col2, col3 = st.columns(3)
    x = col1.number_input("Valor x", value=70.0)
    mu = col2.number_input("Media μ", value=65.0)
    sigma = col3.number_input("Desviación estándar σ", min_value=0.0001, value=5.0)
    if st.button("Calcular P(X ≤ x)"):
        z = (x - mu) / sigma
        prob = 0.5 * (1 + math.erf(z / math.sqrt(2)))
        st.write(f"**Puntaje z:** z = (x − μ) / σ = ({x} − {mu}) / {sigma} = **{z:.4f}**")
        st.write(f"**Probabilidad acumulada:** P(X ≤ {x}) = **{prob:.4f} ({prob*100:.2f}%)**")

with tabs[4]:
    st.header("Correlación lineal y regresión lineal simple")
    x_raw = st.text_input("Valores de X separados por comas", "1, 2, 3, 4, 5")
    y_raw = st.text_input("Valores de Y separados por comas", "2, 3, 5, 4, 6")
    if st.button("Calcular correlación y regresión"):
        try:
            xs, ys = parse_data(x_raw), parse_data(y_raw)
            if len(xs) != len(ys):
                st.error("X e Y deben tener la misma cantidad de datos.")
            elif len(xs) < 2:
                st.error("Ingresa al menos dos pares de datos.")
            elif np.std(xs) == 0 or np.std(ys) == 0:
                st.error("No se puede calcular correlación si X o Y no varían.")
            else:
                r = float(np.corrcoef(xs, ys)[0, 1])
                slope, intercept = np.polyfit(xs, ys, 1)
                st.write(f"**Correlación de Pearson:** r = **{r:.4f}**")
                st.write(f"**Recta de regresión:** ŷ = {slope:.4f}x + {intercept:.4f}")
                if r > 0.7:
                    interp = "relación lineal positiva fuerte."
                elif r > 0.3:
                    interp = "relación lineal positiva moderada."
                elif r < -0.7:
                    interp = "relación lineal negativa fuerte."
                elif r < -0.3:
                    interp = "relación lineal negativa moderada."
                else:
                    interp = "relación lineal débil o cercana a cero."
                st.info("Interpretación aproximada: " + interp)
                fig, ax = plt.subplots()
                ax.scatter(xs, ys, label="Datos")
                xline = np.linspace(min(xs), max(xs), 100)
                ax.plot(xline, slope*xline + intercept, label="Regresión")
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.legend()
                st.pyplot(fig)
        except ValueError as e:
            st.error(str(e))

with tabs[5]:
    st.header("Práctica con retroalimentación")
    questions = [
        {"q": "¿Cuál es la media de 2, 4 y 6?", "options": ["3", "4", "6"], "answer": "4", "why": "Media = (2 + 4 + 6) / 3 = 12 / 3 = 4."},
        {"q": "¿Cuál es la mediana de 1, 3 y 9?", "options": ["1", "3", "9"], "answer": "3", "why": "Los datos ya están ordenados y el valor central es 3."},
        {"q": "¿Cuál es el rango de 5, 8 y 12?", "options": ["7", "8", "17"], "answer": "7", "why": "Rango = máximo − mínimo = 12 − 5 = 7."},
        {"q": "Si 2 de 8 resultados son favorables, ¿cuál es P(A)?", "options": ["0.25", "0.5", "0.8"], "answer": "0.25", "why": "P(A) = 2/8 = 0.25 = 25%."},
        {"q": "¿Qué describe la desviación estándar?", "options": ["El dato mayor", "La dispersión respecto a la media", "La cantidad de datos"], "answer": "La dispersión respecto a la media", "why": "Una desviación estándar mayor suele indicar datos más dispersos respecto de la media."},
        {"q": "¿Cuál es la media de 10, 10, 10?", "options": ["0", "10", "30"], "answer": "10", "why": "Media = (10 + 10 + 10) / 3 = 10."},
        {"q": "¿Qué valor tiene z si x=70, μ=60 y σ=5?", "options": ["2", "10", "14"], "answer": "2", "why": "z = (70 − 60) / 5 = 2."},
        {"q": "Si r está cerca de 1, la correlación lineal es…", "options": ["Positiva fuerte", "Negativa fuerte", "Nula"], "answer": "Positiva fuerte", "why": "Un coeficiente r cercano a +1 indica una relación lineal positiva fuerte."},
        {"q": "¿Cuántos datos mínimos se necesitan para la desviación estándar muestral?", "options": ["1", "2", "0"], "answer": "2", "why": "La fórmula muestral divide entre n−1, por lo que se necesitan al menos dos datos."},
        {"q": "¿Cuál es la frecuencia relativa si 3 de 12 datos son iguales?", "options": ["0.25", "0.5", "4"], "answer": "0.25", "why": "Frecuencia relativa = 3/12 = 0.25 = 25%."}
    ]
    if "practice_order" not in st.session_state:
        st.session_state.practice_order = list(range(len(questions)))
    if st.button("Generar nueva práctica"):
        st.session_state.practice_order = random.sample(range(len(questions)), len(questions))
        st.session_state.pop("practice_answers", None)
    answers = {}
    with st.form("practice_form"):
        for i, idx in enumerate(st.session_state.practice_order):
            q = questions[idx]
            answers[str(idx)] = st.radio(f"{i+1}. {q['q']}", q["options"], key=f"q_{idx}")
        submitted = st.form_submit_button("Revisar respuestas")
    if submitted:
        score = 0
        for idx in st.session_state.practice_order:
            q = questions[idx]
            selected = answers[str(idx)]
            if selected == q["answer"]:
                score += 1
                st.success(f"Correcto: {q['q']} {q['why']}")
            else:
                st.error(f"Incorrecto: {q['q']} Respuesta correcta: **{q['answer']}**. {q['why']}")
        st.metric("Puntuación", f"{score}/{len(questions)}", f"{score/len(questions)*100:.0f}%")

with tabs[6]:
    st.header("10 ejercicios de ejemplo")
    examples = [
        ("Media", "Datos: 4, 6, 8", "Media = (4 + 6 + 8) / 3 = 6."),
        ("Mediana", "Datos: 2, 7, 9", "Datos ordenados: 2, 7, 9. Mediana = 7."),
        ("Moda", "Datos: 1, 2, 2, 3", "El 2 aparece más veces; moda = 2."),
        ("Rango", "Datos: 3, 10, 12", "Rango = 12 − 3 = 9."),
        ("Varianza poblacional", "Datos: 2, 4, 6; media = 4", "σ² = [(2−4)²+(4−4)²+(6−4)²]/3 = 8/3 ≈ 2.6667."),
        ("Desviación estándar muestral", "Datos: 2, 4, 6; media = 4", "s² = [4+0+4]/(3−1) = 4; s = √4 = 2."),
        ("Probabilidad", "Una moneda justa: obtener cara", "P(cara) = 1/2 = 0.5 = 50%."),
        ("Puntaje z", "x = 80, μ = 70, σ = 5", "z = (80−70)/5 = 2."),
        ("Frecuencia relativa", "El valor 3 aparece 4 veces en 20 datos", "fr = 4/20 = 0.20 = 20%."),
        ("Regresión simple", "Pares (1,2), (2,4), (3,6)", "Los puntos siguen ŷ = 2x; pendiente = 2 e intercepto = 0.")
    ]
    for i, (title, problem, solution) in enumerate(examples, 1):
        with st.expander(f"Ejercicio {i}: {title}"):
            st.write(problem)
            st.write("**Procedimiento / respuesta:** " + solution)

st.divider()
st.caption("Proyecto académico de Estadística Aplicada. Verifica los resultados y explica los procedimientos durante la demostración.")
