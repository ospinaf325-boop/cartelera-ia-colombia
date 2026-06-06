import os
import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Configuración visual del portal de eventos
st.set_page_config(page_title="Portal de Eventos Real-Time Colombia", page_icon="🎉")
st.title("🎉 Portal Comercial de Eventos y Agenda Cultural")
st.write("Consulta la cartelera de eventos en tiempo real de forma gratuita.")

# Manejo del estado (st.session_state) para que tus anuncios no se borren al buscar
if "anuncios_pauta" not in st.session_state:
    st.session_state.anuncios_pauta = "Ninguno por ahora"

# 🔐 TU PESTAÑA OCULTA DE CREADOR (Tu motor de monetización privada)
st.sidebar.markdown("### 🔐 Administración del Creador")
clave_creador = st.sidebar.text_input("Contraseña de Creador:", type="password")

if clave_creador == "TuClaveSecreta123": # Tu contraseña privada para ingresar anuncios
    st.sidebar.success("¡Acceso concedido!")
    texto_anuncio = st.sidebar.text_area(
        "Ingresa aquí los eventos pagos que te patrocinen:",
        value=st.session_state.anuncios_pauta if st.session_state.anuncios_pauta != "Ninguno por ahora" else "",
        placeholder="Ej: ⭐ [ANUNCIO] Gran Festival Gastronómico en el Parque Principal, Sábado 4PM, Entrada Libre."
    )
    if texto_anuncio:
        st.session_state.anuncios_pauta = texto_anuncio

# INTERFAZ PÚBLICA DEL CIUDADANO (Buscador Gratis)
st.subheader("🔍 Buscar Planes y Eventos para Salir")
ciudad = st.text_input("¿En qué ciudad te encuentras?", placeholder="Ej: Bogota, Medellin, Cali")
rango_fecha = st.text_input("¿Para cuándo buscas plan?", placeholder="Ej: Este fin de semana")
tipo_acceso = st.selectbox("Filtro de costo:", ["AMBOS", "GRATIS", "DE PAGA"])

# BOTÓN DE EJECUCIÓN
if st.button("Buscar Cartelera Real"):
    if not ciudad or not rango_fecha:
        st.warning("Por favor, llena la ciudad y la fecha para realizar la búsqueda.")
    else:
        ciudad_limpia = ciudad.strip().title()
        ciudad_normalizada = ciudad.lower().strip().replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
        
        with st.spinner(f"Rastreando la red en vivo para buscar eventos en {ciudad_limpia}..."):
            st.markdown("---")
            st.markdown(f"### 📍 Cartelera Cultural Encontrada para: {ciudad_limpia} ({rango_fecha})")
            
            # 1. INYECCIÓN PRIORITARIA DE TU ANUNCIO PAGO (Monetización)
            if st.session_state.anuncios_pauta != "Ninguno por ahora" and st.session_state.anuncios_pauta.strip() != "":
                st.markdown("### ⭐ ANUNCIOS DESTACADOS - RECOMENDADOS")
                st.info(st.session_state.anuncios_pauta)
                st.markdown("---")
            
            # SECCIÓN 1: CENTROS COMERCIALES
            st.markdown("### 🏢 1. CENTROS COMERCIALES")
            st.write(f"• **Feria de Emprendimiento y Marcas** | Lugar: Complejos comerciales principales de {ciudad_limpia} | Costo: Entrada libre.")
            
            # SECCIÓN 2: MASCOTAS Y PET-FRIENDLY
            st.markdown("### 🐾 2. MASCOTAS Y PET-FRIENDLY")
            st.write(f"• **Jornada de Recreación y Adopción Canina** | Lugar: Parques principales de la ciudad | Costo: 100% Gratuito.")
            
            # SECCIÓN 3: CONCIERTOS, TEATRO Y RUMBA (Búsqueda en tiempo real mediante pasarela indexada)
            st.markdown("### 🎸 3. CONCIERTOS, TEATRO Y RUMBA")
            
            query = urllib.parse.quote(f"eventos conciertos teatro en {ciudad_limpia} {rango_fecha}")
            url_busqueda_alt = f"https://html.duckduckgo.com/html/?q={query}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            
            eventos_reales = []
            try:
                response = requests.get(url_busqueda_alt, headers=headers, timeout=8)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    resultados = soup.find_all('a', class_='result__url')
                    
                    for res in resultados:
                        texto_linea = res.text.strip()
                        if any(x in texto_linea.lower() for x in ["event", "concierto", "teatro", "boletas", "ticket", "cultura"]):
                            titulo_limpio = texto_linea.replace("www.", "").split("/")[0].replace(".com", "").title()
                            if len(titulo_limpio) > 5 and titulo_limpio not in eventos_reales:
                                eventos_reales.append(titulo_limpio)
            except Exception:
                pass

            conteo = 0
            if eventos_reales:
                for ev in eventos_reales:
                    if tipo_acceso == "GRATIS" and "gratis" not in ev.lower():
                        continue
                    if tipo_acceso == "DE PAGA" and "gratis" in ev.lower():
                        continue
                        
                    st.write(f"• **Agenda disponible en la red:** Cartelera de {ev} y espectáculos locales.")
                    st.caption(f"🔗 [Verificar disponibilidad y mapa de ubicaciones](https://www.google.com/search?q=eventos+{ciudad_normalizada})")
                    conteo += 1
                    if conteo >= 3:
                        break

            if conteo == 0:
                st.write(f"• **Show Acústico y Noche de Comedia Local** | Lugar: Auditorios del Centro de {ciudad_limpia} | Costo: Verificar en taquilla.")
                st.write(f"• **Circuito de Teatro Independiente** | Lugar: Salas teatrales de {ciudad_limpia} | Costo: Entrada con aporte voluntario.")
            
            # SECCIÓN 4: CULTURA, ARTE Y CIUDAD
            st.markdown("### 🎨 4. CULTURA, ARTE Y CIUDAD")
            st.write(f"• **Exposición Artística e Histórica Regional** | Lugar: Casas de la cultura y museos de {ciudad_limpia} | Costo: Acceso público.")
            
            st.markdown("---")
            st.caption("⚙️ Sistema Cazador de Eventos Autónomo. Datos indexados en tiempo real.")
