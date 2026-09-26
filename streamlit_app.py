# -*- coding: utf-8 -*-
import flet as ft
from datetime import datetime, timedelta

def main(page: ft.Page):
    page.title = "Panel Nutricional Jovi"
    page.window_width = 390
    page.window_height = 844
    page.window_resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 12
    page.theme_mode = ft.ThemeMode.DARK
    
    if not hasattr(main, "desplazamiento"): main.desplazamiento = 0
    if not hasattr(main, "logistica"): main.logistica = "En Casa"
    if not hasattr(main, "magdalenas"): main.magdalenas = False
    if not hasattr(main, "ayuno_finde"): main.ayuno_finde = True
    if not hasattr(main, "bebida_cena"): main.bebida_cena = "Agua/Vino/Cerveza"
    if not hasattr(main, "pestaña_activa"): main.pestaña_activa = 0

    dias_traduccion = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
    meses_traduccion = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}

    contenido_app = ft.Column(spacing=12, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    def crear_tarjeta_comida(titulo, texto, control_extra=None):
        elementos = [
            ft.Text(titulo, weight=ft.FontWeight.BOLD, size=14, color=ft.colors.BLUE),
            ft.Text(texto, font_family="monospace", size=11, no_wrap=False)
        ]
        if control_extra: elementos.insert(1, control_extra)
        return ft.Card(content=ft.Container(content=ft.Column(elementos, spacing=4), padding=10))

    def render_vista_diaria():
        fecha_real = datetime.now()
        fecha_vis = fecha_real + timedelta(days=main.desplazamiento)
        dia_num = fecha_vis.weekday()
        dia_txt = dias_traduccion[dia_num]
        mes_num = int(fecha_vis.strftime("%m"))
        num_semana = fecha_vis.isocalendar()[1]
        dia_mes = fecha_vis.strftime("%d")
        año = fecha_vis.strftime("%Y")
        mes_txt = meses_traduccion[mes_num]
        
        if mes_num in (12, 1, 2):
            estacion, frutas, verduras = "Invierno", ["Naranja", "Mandarina", "Kiwi", "Naranja", "Mandarina", "Kiwi", "Naranja"], ["Alcachofas [M]", "Cardo [M]", "Coliflor [M]", "Repollo [M]", "Romanesco [M]", "Coliflor [M]", "Alcachofas [M]"]
        elif 3 <= mes_num <= 5:
            estacion, frutas, verduras = "Primavera", ["Fresas", "Nísperos", "Albaricoques", "Cerezas", "Ciruelas", "Fresas", "Cerezas"], ["Espárragos verdes [M]", "Guisantes [M]", "Habas [M]", "Ajos tiernos [M]", "Espárragos verdes [M]", "Guisantes [M]", "Habas [M]"]
        elif 6 <= mes_num <= 8:
            estacion, verduras, frutas = "Verano", ["Pimiento [M]", "Calabacín [M]", "Berenjena [M]", "Tomate rosa [M]", "Calabacín [M]", "Pimiento [M]", "Calabacín [M]"], ["Sandía", "Melón", "Melocotón", "Paraguayo", "Nectarina", "Sandía", "Melón"]
        else:
            estacion, frutas, verduras = "Otoño", ["Pera fresca", "Uvas locales", "Caqui Pérsimon", "Pera fresca", "Uvas locales", "Caqui Pérsimon", "Pera fresca"], ["Espinacas [M]", "Judía verde [M]", "Brócoli [M]", "Acelgas [M]", "Calabaza [M]", "Espinacas [M]", "Judía verde [M]"]

        texto_fecha = f"{dia_txt}, {dia_mes}/{fecha_vis.strftime('%m')}/{año}\nNº: {num_semana} | {estacion} | {mes_txt}"
        
        header = ft.Row(
            controls=[
                ft.IconButton(icon=ft.Icons.ARROW_BACK_IOS, on_click=dia_anterior, icon_color=ft.colors.BLUE),
                ft.Text(texto_fecha, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD, size=13, expand=True),
                ft.IconButton(icon=ft.Icons.ARROW_FORWARD_IOS, on_click=dia_siguiente, icon_color=ft.colors.BLUE),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        contenido_app.controls.append(header)
        contenido_app.controls.append(ft.Divider())

        es_finde = dia_num in (5, 6)
        if not es_finde:
            proteinas_almuerzo = {0: "Lomo a la plancha", 1: "Tortilla con atún", 2: "Pollo a la plancha", 3: "Emperador a la plancha", 4: "Sepia/Chipirones a la plancha"}
            proteinas_cena = {0: "Pechuga de pollo", 1: "Atún al natural (Lata grande)", 2: "Salmón fresco", 3: "Hamburguesa de pavo 90%", 4: "Sardinas en conserva"}
            fruta_hoy = frutas[dia_num]
            verdura_hoy = verduras[dia_num]
            
            radio_logistica = ft.RadioGroup(
                content=ft.Row([ft.Radio(value="En Casa", label="🏠 En Casa"), ft.Radio(value="En Ruta", label="🚚 En Ruta")], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                value=main.logistica, on_change=cambiar_logistica
            )
            contenido_app.controls.append(ft.Text("Logística:", size=13, weight=ft.FontWeight.BOLD))
            contenido_app.controls.append(radio_logistica)

            # CORREGIDO: Eliminado argumento 'size' para evitar fallos
            chk_magdalenas = ft.Checkbox(label="Marcar si comes Magdalenas", value=main.magdalenas, on_change=cambiar_magdalenas)
            txt_desayuno = "☕ Líquido: 125ml Leche entera\n🧁 Sólido: 2 Magdalenas valencianas\n⚠️ Backend: Penalización nocturna aplicada." if main.magdalenas else f"💧 Líquido: Agua fresca\n🍏 Sólido: 150g {fruta_hoy} de temporada\n❌ Alerta: Prohibida la manzana en la mañana."
            contenido_app.controls.append(crear_tarjeta_comida("Desayuno", txt_desayuno, chk_magdalenas))

            prot_alm = proteinas_almuerzo.get(dia_num, "Lomo")
            txt_almuerzo = f"🥩 Proteína: 150g de {prot_alm} [P]\n🥖 Hidratos: 60g de Pan del bar + Cacaos\n🥦 Vegetal: Ensalada de bar + Verduras a la plancha\n🥤 Bebida: 1 Coca-Cola normal fija"
            contenido_app.controls.append(crear_tarjeta_comida("Almuerzo", txt_almuerzo))

            if main.logistica == "En Ruta":
                txt_tarde = "🥩 Almuerzo: Menú de Bar (Pescado o Carne)\n🥗 Vegetal: Ensalada mixta\n🥖 Hidratos: Pan pequeño (30g máximo)\n🔕 Sistema: Merienda estratégica ANULADA."
                tit_tarde = "Comida"
            else:
                txt_tarde = f"🍎 Sólido: 150g de {fruta_hoy} de temporada masticada\n❌ Alerta: Cero zumos."
                tit_tarde = "Merienda"
            contenido_app.controls.append(crear_tarjeta_comida(tit_tarde, txt_tarde))

            hidrato_hoy = "Arroz redondo" if (num_semana + dia_num) % 2 == 0 else "Pasta integral"
            peso_h, peso_p = 80, 150
            extras = "1/2 Aguacate entero + Pan (30g) OK"
            prot_cena_hoy = proteinas_cena.get(dia_num, "Pollo")
            if main.magdalenas: peso_h -= 30
            if main.logistica == "En Ruta": peso_h, peso_p, extras = 50, 75, "🛑 Cero Pan por la noche."

            radio_bebida = ft.RadioGroup(
                content=ft.Row([ft.Radio(value="Agua/Vino/Cerveza", label="🔵 Agua/Vino"), ft.Radio(value="Coca-Cola", label="🔴 Coca-Cola")], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                value=main.bebida_cena, on_change=cambiar_bebida
            )
            if main.bebida_cena == "Coca-Cola": extras = "⚠️ 1/4 Aguacate (reducido) + 🛑 Cero Pan."
            txt_cena = f"🍚 Carbohidrato: {peso_h}g de {hidrato_hoy}\n🥩 Proteína:     {peso_p}g de {prot_cena_hoy}\n🥦 Vegetal:      G: {verdura_hoy} (120g)\n🥑 Grasas/Pan:   {extras}"
            contenido_app.controls.append(crear_tarjeta_comida("Cena", txt_cena, radio_bebida))
        else:
            
            # CORREGIDO: Eliminado argumento 'size' para evitar fallos
            chk_ayuno = ft.Checkbox(label="Ayuno Matutino Activo", value=main.ayuno_finde, on_change=cambiar_ayuno)
            if main.ayuno_finde:
                txt_des_finde = "🤐 Estado: Ayuno matutino activado.\n🎯 Objetivo: Llegar limpio al Almuerzo/Comida."
            else:
                txt_des_finde = "🍳 Desayuno (07:30): 2 Huevos revueltos o en tortilla.\n🥖 Hidratos: Opción controlada sin excesos."
            contenido_app.controls.append(crear_tarjeta_comida("Desayuno", txt_des_finde, chk_ayuno))
            
            txt_alm_finde = "🍽️ Comida Principal (14:00 - 15:00):\n🥩 Plato Principal: Menú Libre Controlado o Comida Familiar.\n🥗 Vegetal: Ensalada mixta abundante de primero.\n⚠️ Regla: Disfrutar con moderación sin reventar el backend."
            contenido_app.controls.append(crear_tarjeta_comida("Almuerzo / Comida", txt_alm_finde))
            
            txt_mer_finde = "🍏 Sólido (18:00): 150g de Fruta fresca Masticada de temporada.\n❌ Alerta: Cero zumos, batidos o snacks procesados."
            contenido_app.controls.append(crear_tarjeta_comida("Merienda", txt_mer_finde))
            
            verdura_finde = "Coliflor (120g) [H]" if dia_txt == "Sábado" else "Calabaza al horno (120g)"
            txt_cena_finde = f"🐟 Proteína Nocturna: Pescado blanco (Merluza/Bacalao) o Tortilla francesa.\n🥦 Vegetal: {verdura_finde} de acompañamiento.\n🍚 Hidratos: Reducidos al mínimo por descanso de fin de semana.\n🛑 Alerta: Cero Pan por la noche."
            contenido_app.controls.append(crear_tarjeta_comida("Cena", txt_cena_finde))

    def render_vista_semanal():
        contenido_app.controls.append(ft.Text("Resumen Semanal: Platos Principales", weight=ft.FontWeight.BOLD, size=14, text_align=ft.TextAlign.CENTER))
        contenido_app.controls.append(ft.Divider(height=1))
        proteinas_almuerzo = ["Lomo a la plancha", "Tortilla con atún", "Pollo a la plancha", "Emperador", "Sepia/Chipirones"]
        proteinas_cena = ["Pechuga de pollo", "Atún al natural", "Salmón fresco", "Hamburguesa pavo", "Sardinas conserva"]
        for i in range(5):
            resumen_dia = f"🥩 Almuerzo: {proteinas_almuerzo[i]}\n🐟 Cena: {proteinas_cena[i]}"
            contenido_app.controls.append(crear_tarjeta_comida(dias_traduccion[i], resumen_dia))
        contenido_app.controls.append(crear_tarjeta_comida("Sábado / Domingo", "🤐 Fin de semana: Modo Ayuno / Menú Principal Libre Controlado"))

    def render_vista_configuracion():
        contenido_app.controls.append(ft.Text("⚙️ Ajustes del Panel", weight=ft.FontWeight.BOLD, size=14, text_align=ft.TextAlign.CENTER))
        contenido_app.controls.append(ft.Divider(height=1))
        entrada_nombre = ft.TextField(label="Nombre del Usuario", value="Jovi", dense=True)
        chk_notif = ft.Checkbox(label="Activar Alertas de Backend", value=True)
        btn_guardar = ft.ElevatedButton("Guardar Configuración")
        config_box = ft.Container(content=ft.Column([entrada_nombre, chk_notif, btn_guardar], spacing=10), padding=10)
        contenido_app.controls.append(config_box)

    def actualizar_interfaz():
        contenido_app.controls.clear()
        if main.pestaña_activa == 0: render_vista_diaria()
        elif main.pestaña_activa == 1: render_vista_semanal()
        elif main.pestaña_activa == 2: render_vista_configuracion()
        page.update()

    def dia_anterior(e): main.desplazamiento -= 1; actualizar_interfaz()
    def dia_siguiente(e): main.desplazamiento += 1; actualizar_interfaz()
    def cambiar_logistica(e): main.logistica = e.control.value; actualizar_interfaz()
    def cambiar_magdalenas(e): main.magdalenas = e.control.value; actualizar_interfaz()
    def cambiar_ayuno(e): main.ayuno_finde = e.control.value; actualizar_interfaz()
    def cambiar_bebida(e): main.bebida_cena = e.control.value; actualizar_interfaz()
    def al_cambiar_pestaña(e): main.pestaña_activa = int(e.control.selected_index); actualizar_interfaz()

    barra_inferior = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.Icons.CALENDAR_VIEW_DAY, label="Hoy"),
            ft.NavigationDestination(icon=ft.Icons.VIEW_WEEK, label="Semana"),
            ft.NavigationDestination(icon=ft.Icons.SETTINGS, label="Configuración"),
        ],
        selected_index=main.pestaña_activa,
        on_change=al_cambiar_pestaña,
        height=65
    )

    page.add(contenido_app, barra_inferior)
    actualizar_interfaz()

ft.app(target=main)

python3 ~/Desktop/app_jovi.py
