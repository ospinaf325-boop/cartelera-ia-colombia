import os
import streamlit as st
from google import genai
from google.genai import types

# Configuración visual de la página en Streamlit
st.set_page_config(page_title="Portal de Eventos IA Colombia", page_icon="🎉")
st.title("🎉 Portal Comercial de Eventos e Inmuebles")
st.write("Consulta la cartelera urbana actual de forma gratuita.")

# Conectar de forma segura la API Key gratuita de Google AI Studio
# Debes meterla en la sección 'Secrets' de Streamlit Cloud como GEMINI_API_KEY
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("Falta configurar la variable secreta GEMINI_API_KEY en Streamlit.")
else:
    client = genai.Client(api_key=API_KEY)

    # INTERFAZ PÚBLICA DEL CIUDADANO (Formulario integrado)
    st.subheader("🔍 Buscar Planes del Fin de Semana")
    ciudad = st.text_input("¿En qué ciudad te encuentras?", placeholder="Ej: Bogotá, Medellín, Cali")
    rango_fecha = st.text_input("¿Para cuándo buscas plan?", placeholder="Ej: Este fin de semana, Próximo viernes")
    tipo_acceso = st.selectbox("Filtro de costo:", ["GRATIS", "DE PAGA", "AMBOS"])

    # 🔑 TU PESTAÑA OCULTA DE CREADOR (Blindada por contraseña visual directa)
    # Solo tú conoces el texto secreto para desbloquear la carga de anuncios
    st.sidebar.markdown("### 🔐 Administración del Creador")
    clave_creador = st.sidebar.text_input("Contraseña de Creador:", type="password")
    
    anuncios_pauta = "Ninguno por ahora"
    if clave_creador == "TuClaveSecreta123": # Cambia esto por tu contraseña privada
        st.sidebar.success("¡Acceso concedido!")
        anuncios_pauta = st.sidebar.text_area(
            "Ingresa aquí tus anuncios pagos (Se guardan en memoria de la sesión):",
            placeholder="Ej: ⭐ [ANUNCIO] Feria Canina en Unicentro Bogotá, Sábado 4PM, Entrada Libre."
        )

    # BOTÓN DE EJECUCIÓN
    if st.button("Buscar Cartelera"):
        if not ciudad or not rango_fecha:
            st.warning("Por favor, llena la ciudad y la fecha para realizar la búsqueda.")
        else:
            with st.spinner("Rastreando la red y organizando la cartelera..."):
                try:
                    # Instrucciones de estructuración y priorización comercial
                    instrucciones = (
                        "Eres el director comercial de la guía de eventos y cartelera urbana más leída de Colombia.\n\n"
                        f"Tu trabajo es generar un reporte de eventos para la ciudad de '{ciudad}' en la fecha '{rango_fecha}', "
                        f"aplicando el filtro de acceso: '{tipo_acceso}'.\n\n"
                        "REGLA DE MONETIZACIÓN (ANUNCIOS PAGOS DE TU PESTAÑA DE CREADOR):\n"
                        f"Desde tu panel privado se han cargado estos eventos VIP patrocinados: '{anuncios_pauta}'.\n"
                        "Si coinciden con la ciudad y fecha, DEBES colocarlos de PRIMEROS en su respectiva categoría, "
                        "resaltados con la etiqueta '⭐ [ANUNCIO DESTACADO - RECOMENDADO]'.\n\n"
                        "Luego, completa el reporte rastreando la red actual y dividiendo todo en estas 4 categorías estrictas:\n"
                        "1. 🏢 CENTROS COMERCIALES\n"
                        "2. 🐾 MASCOTAS Y PET-FRIENDLY\n"
                        "3. 🎸 CONCIERTOS, TEATRO Y RUMBA\n"
                        "4. 🎨 CULTURA, ARTE Y CIUDAD\n\n"
                        "Cada evento listado debe incluir únicamente: Nombre, Lugar, Hora, Precio y el Enlace Oficial."
                    )

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=f"Genera la cartelera temática para {ciudad} integrando mis destacados.",
                        config=types.GenerateContentConfig(
                            system_instruction=instrucciones,
                            temperature=0.3,
                        )
                    )
                    
                    # Mostrar el resultado final limpio en la web
                    st.markdown("---")
                    st.markdown(response.text.strip())
                    
                except Exception as e:
                    st.error(f"Hubo un error al procesar la solicitud: {str(e)}")
