# -*- coding: utf-8 -*-
import streamlit as st
from datetime import datetime, timedelta

# Configuración de la página estilo móvil
st.set_page_config(page_title="Panel Nutricional Jovi", page_icon="🥗", layout="centered")

# CORRECCIÓN: Se cambió 'unsafe_index' por 'unsafe_allow_html'
st.markdown("""
    <style>
    .block-container { max-width: 390px; padding-top: 2rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

# Inicializar estados de la sesión si no existen
if "desplazamiento" not in st.session_state: st.session_state.desplazamiento = 0
if "logistica" not in st.session_state: st.session_state.logistica = "En Casa"
if "magdalenas" not in st.session_state: st.session_state.magdalenas = False
if "ayuno_finde" not in st.session_state: st.session_state.ayuno_finde = True
if "bebida_cena" not in st.session_state: st.session_state.bebida_cena = "Agua/Vino/Cerveza"

# Diccionarios de traducción
dias_traduccion = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
meses_traduccion = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}

# Barra de navegación superior (pestañas nativas de Streamlit)
pestaña = st.tabs(["📅 Hoy", "📊 Semana", "⚙️ Ajustes"])

# ==========================================
# PESTAÑA 1: VISTA DIARIA
# ==========================================
with pestaña[0]:
    fecha_real = datetime.now()
    fecha_vis = fecha_real + timedelta(days=st.session_state.desplazamiento)
    dia_num = fecha_vis.weekday()
    dia_txt = dias_traduccion[dia_num]
    mes_num = int(fecha_vis.strftime("%m"))
    num_semana = fecha_vis.isocalendar()[1]
    dia_mes = fecha_vis.strftime("%d")
    año = fecha_vis.strftime("%Y")
    mes_txt = meses_traduccion[mes_num]

    # Estaciones y alimentos
    if mes_num in (12, 1, 2):
        estacion, frutas, verduras = "Invierno", ["Naranja", "Mandarina", "Kiwi", "Naranja", "Mandarina", "Kiwi", "Naranja"], ["Alcachofas [M]", "Cardo [M]", "Coliflor [M]", "Repollo [M]", "Romanesco [M]", "Coliflor [M]", "Alcachofas [M]"]
    elif 3 <= mes_num <= 5:
        estacion, frutas, verduras = "Primavera", ["Fresas", "Nísperos", "Albaricoques", "Cerezas", "Ciruelas", "Fresas", "Cerezas"], ["Espárragos verdes [M]", "Guisantes [M]", "Habas [M]", "Ajos tiernos [M]", "Espárragos verdes [M]", "Guisantes [M]", "Habas [M]"]
    elif 6 <= mes_num <= 8:
        estacion, verduras, frutas = "Verano", ["Pimiento [M]", "Calabacín [M]", "Berenjena [M]", "Tomate rosa [M]", "Calabacín [M]", "Pimiento [M]", "Calabacín [M]"], ["Sandía", "Melón", "Melocotón", "Paraguayo", "Nectarina", "Sandía", "Melón"]
    else:
        estacion, frutas, verduras = "Otoño", ["Pera fresca", "Uvas locales", "Caqui Pérsimon", "Pera fresca", "Uvas locales", "Caqui Pérsimon", "Pera fresca"], ["Espinacas [M]", "Judía verde [M]", "Brócoli [M]", "Acelgas [M]", "Calabaza [M]", "Espinacas [M]", "Judía verde [M]"]

    # Selector de fecha (Header)
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.button("◀", key="prev"): st.session_state.desplazamiento -= 1; st.rerun()
    with col2:
        texto_fecha = f"**{dia_txt}, {dia_mes}/{fecha_vis.strftime('%m')}/{año}**\n\nNº: {num_semana} | {estacion} | {mes_txt}"
        st.markdown(f"<div style='text-align: center;'>{texto_fecha}</div>", unsafe_allow_html=True)
    with col3:
        if st.button("▶", key="next"): st.session_state.desplazamiento += 1; st.rerun()

    st.divider()

    es_finde = dia_num in (5, 6)
    if not es_finde:
        proteinas_almuerzo = {0: "Lomo a la plancha", 1: "Tortilla con atún", 2: "Pollo a la plancha", 3: "Emperador a la plancha", 4: "Sepia/Chipirones a la plancha"}
        proteinas_cena = {0: "Pechuga de pollo", 1: "Atún al natural (Lata grande)", 2: "Salmón fresco", 3: "Hamburguesa de pavo 90%", 4: "Sardinas en conserva"}
        fruta_hoy = frutas[dia_num]
        verdura_hoy = verduras[dia_num]

        # Logística
        st.write("**Logística:**")
        st.session_state.logistica = st.radio("Selecciona entorno:", ["🏠 En Casa", "🚚 En Ruta"], label_visibility="collapsed", horizontal=True)

        # Desayuno
        st.markdown("### 🔵 Desayuno")
        st.session_state.magdalenas = st.checkbox("Marcar si comes Magdalenas", value=st.session_state.magdalenas)
        if st.session_state.magdalenas:
            txt_desayuno = "☕ Líquido: 125ml Leche entera\n🧁 Sólido: 2 Magdalenas valencianas\n⚠️ Backend: Penalización nocturna aplicada."
        else:
            txt_desayuno = f"💧 Líquido: Agua fresca\n🍏 Sólido: 150g {fruta_hoy} de temporada\n❌ Alerta: Prohibida la manzana en la mañana."
        st.code(txt_desayuno, language="text")

        # Almuerzo
        st.markdown("### 🔵 Almuerzo")
        prot_alm = proteinas_almuerzo.get(dia_num, "Lomo")
        txt_almuerzo = f"🥩 Proteína: 150g de {prot_alm} [P]\n🥖 Hidratos: 60g de Pan del bar + Cacaos\n🥦 Vegetal: Ensalada de bar + Verduras a la plancha\n🥤 Bebida: 1 Coca-Cola normal fija"
        st.code(txt_almuerzo, language="text")

        # Merienda / Comida Ruta
        if st.session_state.logistica == "🚚 En Ruta":
            st.markdown("### 🔵 Comida")
            txt_tarde = "🥩 Almuerzo: Menú de Bar (Pescado o Carne)\n🥗 Vegetal: Ensalada mixta\n🥖 Hidratos: Pan pequeño (30g máximo)\n🔕 Sistema: Merienda estratégica ANULADA."
        else:
            st.markdown("### 🔵 Merienda")
            txt_tarde = f"🍎 Sólido: 150g de {fruta_hoy} de temporada masticada\n❌ Alerta: Cero zumos."
        st.code(txt_tarde, language="text")

        # Cena
        st.markdown("### 🔵 Cena")
        st.write("**Bebida Cena:**")
        st.session_state.bebida_cena = st.radio("Selecciona bebida:", ["🔵 Agua/Vino", "🔴 Coca-Cola"], label_visibility="collapsed", horizontal=True)

        hidrato_hoy = "Arroz redondo" if (num_semana + dia_num) % 2 == 0 else "Pasta integral"
        peso_h, peso_p = 80, 150
        extras = "1/2 Aguacate entero + Pan (30g) OK"
        prot_cena_hoy = proteinas_cena.get(dia_num, "Pollo")
        
        if st.session_state.magdalenas: peso_h -= 30
        if st.session_state.logistica == "🚚 En Ruta": peso_h, peso_p, extras = 50, 75, "🛑 Cero Pan por la noche."
        if st.session_state.bebida_cena == "🔴 Coca-Cola": extras = "⚠️ 1/4 Aguacate (reducido) + 🛑 Cero Pan."
        
        txt_cena = f"🍚 Carbohidrato: {peso_h}g de {hidrato_hoy}\n🥩 Proteína:     {peso_p}g de {prot_cena_hoy}\n🥦 Vegetal:      G: {verdura_hoy} (120g)\n🥑 Grasas/Pan:   {extras}"
        st.code(txt_cena, language="text")

    else:
        # Fin de semana
        st.markdown("### 🔵 Desayuno")
        st.session_state.ayuno_finde = st.checkbox("Ayuno Matutino Activo", value=st.session_state.ayuno_finde)
        if st.session_state.ayuno_finde:
            txt_des_finde = "🤐 Estado: Ayuno matutino activado.\n🎯 Objetivo: Llegar limpio al Almuerzo/Comida."
        else:
            txt_des_finde = "🍳 Desayuno (07:30): 2 Huevos revueltos o en tortilla.\n🥖 Hidratos: Opción controlada sin excesos."
        st.code(txt_des_finde, language="text")
        
        st.markdown("### 🔵 Almuerzo / Comida")
        txt_alm_finde = "🍽️ Comida Principal (14:00 - 15:00):\n🥩 Plato Principal: Menú Libre Controlado o Comida Familiar.\n🥗 Vegetal: Ensalada mixta abundante de primero.\n⚠️ Regla: Disfrutar con moderación sin reventar el backend."
        st.code(txt_alm_finde, language="text")
        
        st.markdown("### 🔵 Merienda")
        txt_mer_finde = "🍏 Sólido (18:00): 150g de Fruta fresca Masticada de temporada.\n❌ Alerta: Cero zumos, batidos o snacks procesados."
        st.code(txt_mer_finde, language="text")
        
        st.markdown("### 🔵 Cena")
        verdura_finde = "Coliflor (120g) [H]" if dia_txt == "Sábado" else "Calabaza al horno (120g)"
        txt_cena_finde = f"🐟 Proteína Nocturna: Pescado blanco (Merluza/Bacalao) o Tortilla francesa.\n🥦 Vegetal: {verdura_finde} de acompañamiento.\n🍚 Hidratos: Reducidos al mínimo por descanso de fin de semana.\n🛑 Alerta: Cero Pan por la noche."
        st.code(txt_cena_finde, language="text")

# ==========================================
# PESTAÑA 2: RESUMEN SEMANAL
# ==========================================
with pestaña[1]:
    st.markdown("### 📊 Resumen Semanal: Platos Principales")
    st.divider()
    proteinas_almuerzo = ["Lomo a la plancha", "Tortilla con atún", "Pollo a la plancha", "Emperador", "Sepia/Chipirones"]
    proteinas_cena = ["Pechuga de pollo", "Atún al natural", "Salmón fresco", "Hamburguesa pavo", "Sardinas conserva"]
    
    for i in range(5):
        st.markdown(f"**{dias_traduccion[i]}**")
        resumen_dia = f"🥩 Almuerzo: {proteinas_almuerzo[i]}\n🐟 Cena: {proteinas_cena[i]}"
        st.code(resumen_dia, language="text")
    st.markdown("**Sábado / Domingo**")
    st.code("🤐 Fin de semana: Modo Ayuno / Menú Principal Libre Controlado", language="text")

# ==========================================
# PESTAÑA 3: CONFIGURACIÓN
# ==========================================
with pestaña[2]:
    st.markdown("### ⚙️ Ajustes del Panel")
    st.divider()
    entrada_nombre = st.text_input("Nombre del Usuario", value="Jovi")
    chk_notif = st.checkbox("Activar Alertas de Backend", value=True)
    if st.button("Guardar Configuración"):
        st.success(f"¡Configuración de {entrada_nombre} guardada con éxito!")
