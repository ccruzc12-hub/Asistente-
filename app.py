import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog
import random
import math

st.set_page_config(page_title="IO Fácil | Asistente académico", page_icon="📊", layout="wide")

st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#f4f8ff 0%,#fff8ef 100%); color:#172033;}
/* Fuerza texto oscuro en el área principal para evitar letras blancas sobre fondo claro */
[data-testid="stAppViewContainer"] .main,
[data-testid="stAppViewContainer"] .main p,
[data-testid="stAppViewContainer"] .main label,
[data-testid="stAppViewContainer"] .main li,
[data-testid="stAppViewContainer"] .main h1,
[data-testid="stAppViewContainer"] .main h2,
[data-testid="stAppViewContainer"] .main h3,
[data-testid="stAppViewContainer"] .main h4,
[data-testid="stAppViewContainer"] .main [data-testid="stMarkdownContainer"],
[data-testid="stAppViewContainer"] .main [data-testid="stMarkdownContainer"] p,
[data-testid="stAppViewContainer"] .main [data-testid="stMarkdownContainer"] strong {color:#172033;}
[data-testid="stAppViewContainer"] .main [data-testid="stAlert"] p {color:#172033;}
[data-testid="stAppViewContainer"] .main .hero,
[data-testid="stAppViewContainer"] .main .hero h1,
[data-testid="stAppViewContainer"] .main .hero p {color:#ffffff;}
[data-testid="stHeader"] {background: rgba(0,0,0,0);}
.hero {padding: 22px 26px; border-radius: 18px; color:white;
background: linear-gradient(100deg,#123b70,#087e8b,#24a19c); margin-bottom:18px;}
.hero h1 {margin:0; font-size:2.2rem;}
.hero p {margin:6px 0 0 0; font-size:1rem;}
div[data-testid="stMetric"] {background:white; padding:14px; border-radius:12px; border:1px solid #dce7f4;}
.card {background:white; padding:16px; border-radius:14px; border-left:5px solid #f4a261; margin:8px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>📊 IO Fácil</h1>
<p>Asistente virtual de Investigación de Operaciones · Aprende con fórmulas, cálculos y ejemplos</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎓 Datos académicos")
    st.write("**Universidad:** Mariano Gálvez de Guatemala")
    st.write("**Facultad:** Ingeniería, Matemática y Ciencias Físicas")
    st.write("**Asignatura:** Investigación de Operaciones")
    st.write("**Sección:** A")
    st.markdown("---")
    st.write("**Cristopher Francisco Cruz Cardona**")
    st.caption("Carné: 2990-24-19768")
    st.write("**Pablo Andre Díaz Salazar**")
    st.caption("Carné: 2990-24-15879")
    st.markdown("---")
    st.caption("Proyecto académico · Python + Streamlit")

st.info("Escribe datos nuevos en los formularios. Los resultados son educativos: revisa las unidades y las condiciones de cada problema.")

modulo = st.selectbox("¿Qué deseas resolver?", [
    "Inicio y 10 ejemplos", "Modelación de problemas", "Programación lineal (2 variables)",
    "Método gráfico", "Método simplex (ejemplo básico)", "Transporte y asignación",
    "Inventarios: EOQ y punto de reorden", "Práctica con retroalimentación"
])

def solve_lp(c, A, b, maximize=True):
    # linprog minimiza; para maximizar se cambia el signo de c
    obj = [-v for v in c] if maximize else list(c)
    res = linprog(obj, A_ub=A, b_ub=b, bounds=[(0, None)]*len(c), method="highs")
    return res

if modulo == "Inicio y 10 ejemplos":
    st.subheader("🌟 Bienvenido a IO Fácil")
    st.write("Utiliza los módulos para modelar y resolver problemas típicos de Investigación de Operaciones.")
    examples = [
        ("Mezcla de productos", "Maximizar ganancia con horas de trabajo y materia prima limitadas."),
        ("Producción", "Elegir cantidades de dos productos sin superar la capacidad de las máquinas."),
        ("Dieta", "Minimizar costo cumpliendo requerimientos nutricionales."),
        ("Transporte", "Distribuir productos desde fábricas hacia destinos con costo mínimo."),
        ("Asignación", "Asignar trabajadores a tareas con el menor costo total."),
        ("Inventario EOQ", "Calcular el tamaño económico de pedido."),
        ("Punto de reorden", "Determinar cuándo volver a pedir mercancía."),
        ("Horas de máquina", "Distribuir tiempo disponible entre trabajos."),
        ("Publicidad", "Asignar presupuesto entre medios para maximizar alcance."),
        ("Planificación", "Seleccionar una combinación factible de recursos.")
    ]
    for i in range(0,10,2):
        a,b=st.columns(2)
        for col, item in zip((a,b), examples[i:i+2]):
            with col:
                st.markdown(f'<div class="card"><b>{i+1 if col==a else i+2}. {item[0]}</b><br>{item[1]}</div>', unsafe_allow_html=True)
    st.markdown("### Ejemplo resuelto solicitado en la guía")
    st.latex(r"\\max Z=40x+30y")
    st.latex(r"2x+y\\leq100,\\quad x+2y\\leq80,\\quad x,y\\geq0")
    res=solve_lp([40,30], [[2,1],[1,2]],[100,80],True)
    if res.success:
        x,y=res.x
        st.success(f"Solución óptima: x = {x:.2f}, y = {y:.2f}, Z = {40*x+30*y:.2f}")
        st.write("Interpretación: esta combinación maximiza Z respetando ambas restricciones. En este caso, el óptimo se encuentra en la intersección de las restricciones.")

elif modulo in ["Programación lineal (2 variables)", "Método gráfico"]:
    st.subheader("🧮 Programación lineal con dos variables")
    c1,c2=st.columns(2)
    with c1:
        st.markdown("#### Función objetivo")
        cx=st.number_input("Coeficiente de x", value=40.0)
        cy=st.number_input("Coeficiente de y", value=30.0)
        sentido=st.radio("Objetivo", ["Maximizar","Minimizar"], horizontal=True)
    with c2:
        st.markdown("#### Restricciones (formato ≤)")
        a11=st.number_input("Restricción 1: coeficiente de x",value=2.0)
        a12=st.number_input("Restricción 1: coeficiente de y",value=1.0)
        b1=st.number_input("Límite de restricción 1",value=100.0)
        a21=st.number_input("Restricción 2: coeficiente de x",value=1.0)
        a22=st.number_input("Restricción 2: coeficiente de y",value=2.0)
        b2=st.number_input("Límite de restricción 2",value=80.0)
    if st.button("Resolver problema", type="primary"):
        if min(a11,a12,a21,a22,b1,b2) < 0 or (a11==0 and a12==0) or (a21==0 and a22==0):
            st.error("Verifica los datos: usa coeficientes no negativos y cada restricción debe tener al menos un coeficiente distinto de cero.")
        else:
            res=solve_lp([cx,cy],[[a11,a12],[a21,a22]],[b1,b2],sentido=="Maximizar")
            if res.success:
                x,y=res.x; z=cx*x+cy*y
                st.success("Problema resuelto correctamente.")
                m1,m2,m3=st.columns(3)
                m1.metric("x óptima",f"{x:.3f}"); m2.metric("y óptima",f"{y:.3f}"); m3.metric("Valor Z",f"{z:.3f}")
                st.markdown("**Fórmula:** Z = c₁x + c₂y")
                st.markdown(f"**Sustitución:** Z = ({cx:g})({x:.3f}) + ({cy:g})({y:.3f}) = **{z:.3f}**")
                st.write("**Procedimiento:** se optimiza la función objetivo respetando las restricciones y las condiciones x ≥ 0, y ≥ 0.")
                st.write("**Interpretación:** la combinación calculada es la mejor encontrada por el modelo bajo los datos ingresados.")
                xx=np.linspace(0,max(b1/max(a11,0.01),b2/max(a21,0.01),x,1)*1.2,300)
                fig,ax=plt.subplots()
                for aa,bb,lim,label in [(a11,a12,b1, "Restricción 1"),(a21,a22,b2,"Restricción 2")]:
                    if bb>0 and aa>=0 and bb>=0:
                        if bb>0 and aa==0:
                            ax.axhline(lim/bb,label=label)
                        elif bb>0:
                            yy=(lim-aa*xx)/bb
                            yy=np.where(yy>=0,yy,np.nan)
                            ax.plot(xx,yy,label=label)
                ax.scatter([x],[y],s=90,label="Óptimo")
                ax.set_xlim(left=0); ax.set_ylim(bottom=0); ax.set_xlabel("x"); ax.set_ylabel("y")
                ax.set_title("Visualización de restricciones"); ax.grid(alpha=.25); ax.legend()
                st.pyplot(fig)
            else:
                st.warning("No se encontró una solución óptima con estos datos. Puede que el problema sea infactible o no esté acotado.")

elif modulo == "Modelación de problemas":
    st.subheader("🧩 Asistente de modelación")
    st.write("Completa los datos del problema y organiza las variables, objetivo y restricciones.")
    nombrex=st.text_input("¿Qué representa x?", "Cantidad del producto A")
    nombrey=st.text_input("¿Qué representa y?", "Cantidad del producto B")
    objx=st.number_input("Ganancia/costo por unidad de x",value=40.0)
    objy=st.number_input("Ganancia/costo por unidad de y",value=30.0)
    r1x=st.number_input("Recurso 1 usado por x",value=2.0)
    r1y=st.number_input("Recurso 1 usado por y",value=1.0)
    r1b=st.number_input("Disponibilidad del recurso 1",value=100.0)
    r2x=st.number_input("Recurso 2 usado por x",value=1.0)
    r2y=st.number_input("Recurso 2 usado por y",value=2.0)
    r2b=st.number_input("Disponibilidad del recurso 2",value=80.0)
    objetivo=st.radio("Tipo de objetivo",["Maximizar ganancia","Minimizar costo"])
    if st.button("Construir modelo",type="primary"):
        if min(r1x,r1y,r1b,r2x,r2y,r2b)<0:
            st.error("Los datos de recursos y disponibilidades no pueden ser negativos.")
        else:
            st.markdown("**Variables de decisión**")
            st.write(f"x = {nombrex}; y = {nombrey}.")
            st.markdown("**Función objetivo**")
            st.latex(r"Z="+f"{objx:g}x+{objy:g}y")
            st.markdown("**Restricciones**")
            st.latex(f"{r1x:g}x+{r1y:g}y\\leq{r1b:g}")
            st.latex(f"{r2x:g}x+{r2y:g}y\\leq{r2b:g}")
            st.latex(r"x\\geq0,\\quad y\\geq0")
            st.caption("Modelo construido con la suposición de que los recursos disponibles son límites de tipo ≤.")

elif modulo == "Método simplex (ejemplo básico)":
    st.subheader("📐 Método simplex: ejemplo básico")
    st.write("Para mantener el procedimiento transparente, este módulo presenta un ejemplo de maximización con holguras y verifica el óptimo mediante un solucionador lineal.")
    st.latex(r"\\max Z=3x+5y")
    st.latex(r"x\\leq4,\\quad 2y\\leq12,\\quad 3x+2y\\leq18,\\quad x,y\\geq0")
    if st.button("Mostrar solución y procedimiento",type="primary"):
        res=solve_lp([3,5],[[1,0],[0,2],[3,2]],[4,12,18],True)
        if res.success:
            x,y=res.x
            st.write("**Paso 1.** Convertir las restricciones ≤ en igualdades agregando variables de holgura.")
            st.latex(r"x+s_1=4,\\quad 2y+s_2=12,\\quad 3x+2y+s_3=18")
            st.write("**Paso 2.** Construir la tabla inicial y seleccionar variables entrantes/salientes según el criterio simplex.")
            st.write("**Paso 3.** Realizar pivotes hasta que no exista mejora en Z.")
            st.success(f"Óptimo verificado: x = {x:.2f}, y = {y:.2f}, Z = {3*x+5*y:.2f}")
            st.caption("El módulo explica las etapas y verifica numéricamente el óptimo; no despliega cada tabla pivote intermedia.")

elif modulo == "Transporte y asignación":
    st.subheader("🚚 Transporte y asignación")
    tipo=st.radio("Tipo de problema",["Transporte 2×2","Asignación 2×2"],horizontal=True)
    st.write("Introduce los costos unitarios.")
    c11=st.number_input("Costo A→1",value=4.0); c12=st.number_input("Costo A→2",value=6.0)
    c21=st.number_input("Costo B→1",value=5.0); c22=st.number_input("Costo B→2",value=3.0)
    if tipo=="Transporte 2×2":
        sa=st.number_input("Oferta origen A",value=30.0); sb=st.number_input("Oferta origen B",value=20.0)
        d1=st.number_input("Demanda destino 1",value=25.0); d2=st.number_input("Demanda destino 2",value=25.0)
        if st.button("Calcular transporte",type="primary"):
            if min(sa,sb,d1,d2)<0: st.error("Oferta y demanda deben ser no negativas.")
            elif abs(sa+sb-d1-d2)>1e-6: st.error("El modelo requiere oferta total igual a demanda total. Balancea los datos primero.")
            else:
                # variable order x11,x12,x21,x22
                Aeq=[[1,1,0,0],[0,0,1,1],[1,0,1,0],[0,1,0,1]]
                beq=[sa,sb,d1,d2]
                rr=linprog([c11,c12,c21,c22],A_eq=Aeq,b_eq=beq,bounds=(0,None),method="highs")
                if rr.success:
                    st.success(f"Costo total mínimo: {rr.fun:.2f}")
                    st.write(f"A→1: {rr.x[0]:.2f} | A→2: {rr.x[1]:.2f} | B→1: {rr.x[2]:.2f} | B→2: {rr.x[3]:.2f}")
                    st.write("Procedimiento: se minimiza la suma de costo unitario × cantidad enviada, cumpliendo oferta y demanda.")
    else:
        if st.button("Resolver asignación",type="primary"):
            rr=linprog([c11,c12,c21,c22],A_eq=[[1,1,0,0],[0,0,1,1],[1,0,1,0],[0,1,0,1]],b_eq=[1,1,1,1],bounds=(0,None),method="highs")
            if rr.success:
                st.success(f"Costo mínimo de asignación: {rr.fun:.2f}")
                st.write("Trabajador A → tarea 1" if rr.x[0]>.5 else "Trabajador A → tarea 2")
                st.write("Trabajador B → tarea 1" if rr.x[2]>.5 else "Trabajador B → tarea 2")
                st.caption("Modelo ilustrativo de asignación uno a uno con costos ingresados.")

elif modulo == "Inventarios: EOQ y punto de reorden":
    st.subheader("📦 Gestión de inventarios")
    D=st.number_input("Demanda anual (unidades)",min_value=0.0,value=1200.0)
    S=st.number_input("Costo por pedido",min_value=0.0,value=25.0)
    H=st.number_input("Costo anual de mantener una unidad",min_value=0.0,value=4.0)
    d=st.number_input("Demanda promedio diaria",min_value=0.0,value=5.0)
    L=st.number_input("Tiempo de entrega (días)",min_value=0.0,value=6.0)
    if st.button("Calcular inventario",type="primary"):
        if H==0:
            st.error("El costo de mantener inventario H debe ser mayor que cero para calcular EOQ.")
        else:
            q=math.sqrt(2*D*S/H) if D>0 and S>=0 else 0
            r=d*L
            st.metric("EOQ (cantidad económica de pedido)",f"{q:.2f} unidades")
            st.metric("Punto de reorden",f"{r:.2f} unidades")
            st.markdown("**Fórmula EOQ:**")
            st.latex(r"Q^*=\\sqrt{\\frac{2DS}{H}}")
            st.write(f"Sustitución: Q* = √(2 × {D:g} × {S:g} / {H:g}) = **{q:.2f}**")
            st.markdown("**Fórmula del punto de reorden:**")
            st.latex(r"R=d\\times L")
            st.write(f"Sustitución: R = {d:g} × {L:g} = **{r:.2f} unidades**")
            st.caption("Se supone demanda y plazo de entrega constantes, sin inventario de seguridad.")

elif modulo == "Práctica con retroalimentación":
    st.subheader("🎯 Práctica con retroalimentación")
    preguntas=[
        ("Si D=500, S=20 y H=5, ¿cuál es el EOQ aproximado?", math.sqrt(2*500*20/5), "Usa Q*=√(2DS/H)."),
        ("Si la demanda diaria es 8 y el plazo de entrega 4 días, ¿cuál es R?", 32, "Usa R=d×L."),
        ("En Z=7x+2y, ¿cuál es el coeficiente de x?", 7, "Es el número que multiplica a x."),
        ("Si x≥0 y y≥0, ¿qué tipo de condición es?", "no negatividad", "Las variables de decisión no pueden ser negativas.")
    ]
    if "preg_idx" not in st.session_state: st.session_state.preg_idx=0
    if "score" not in st.session_state: st.session_state.score=0
    idx=st.session_state.preg_idx % len(preguntas)
    q,ans,hint=preguntas[idx]
    st.markdown(f"**Pregunta {idx+1} de {len(preguntas)}**")
    st.write(q)
    respuesta=st.text_input("Tu respuesta",key=f"answer_{st.session_state.preg_idx}")
    if st.button("Comprobar respuesta",type="primary"):
        correcto=False
        try:
            if isinstance(ans,str): correcto=respuesta.strip().lower()==ans
            else: correcto=abs(float(respuesta)-ans)<0.15
        except ValueError: correcto=False
        if correcto:
            st.success("¡Correcto! Buen trabajo.")
            st.session_state.score+=1
        else:
            st.warning(f"Aún no. Pista: {hint} Respuesta esperada: {ans:.2f}" if not isinstance(ans,str) else f"Aún no. Pista: {hint} Respuesta esperada: {ans}")
        st.session_state.preg_idx+=1
        st.rerun()
    st.caption(f"Aciertos acumulados en esta sesión: {st.session_state.score}")

st.markdown("---")
st.caption("IO Fácil · Herramienta académica para practicar Investigación de Operaciones. Los resultados dependen de los datos ingresados.")
