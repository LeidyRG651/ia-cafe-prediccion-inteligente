# --- Importaciones ---
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
from sklearn.linear_model import LinearRegression
import pandas as pd
from datetime import datetime
from telegram.ext import CallbackQueryHandler


# --- Configuración Inicial ---
# Entrenar modelo de predicción
data = pd.DataFrame({
    'ph_suelo': [5.0, 6.0, 6.5, 7.0, 5.5],
    'fertilizante': [10, 20, 30, 40, 15],
    'rendimiento': [500, 800, 1200, 1500, 600]
})
modelo = LinearRegression().fit(data[['ph_suelo', 'fertilizante']], data['rendimiento'])

# --- Función de Predicción ---
def predecir_rendimiento(ph, fertilizante):
    # Predicción con el modelo de regresión
    prediccion = modelo.predict([[ph, fertilizante]])[0]
    
    return f"📊 El rendimiento estimado es: {prediccion:.2f} kg de café por hectárea."

# --- Base de Conocimiento Mejorada ---
# --- Respuestas rápidas ---
respuestas = {
    "suelo": (
        "🌱 <b>Información sobre el suelo</b>\n\n"
        "• pH ideal: 5.5 - 6.5\n"
        "• Textura: franca o franco-arenosa\n"
        "• Rica en materia orgánica\n\n"
        "💡 Suelo bien drenado favorece el crecimiento del café"
    ),
    "clima": (
        "🌤️ <b>Condiciones climáticas óptimas</b>\n\n"
        "• Temperatura: 18°C - 24°C\n"
        "• Precipitación: 1200-2000 mm/año\n"
        "• Altitud: 1200-2000 m.s.n.m\n\n"
        "🌦️ Clima estable = mayor rendimiento"
    ),
    "fertilizante": (
        "🌿 <b>Recomendaciones de fertilización</b>\n\n"
        "• Nitrógeno: estimula el crecimiento\n"
        "• Fósforo: favorece raíces fuertes\n"
        "• Potasio: mejora calidad del grano\n\n"
        "📆 Aplicar 3 veces por ciclo productivo"
    ),
    "plagas": (
        "🐛 <b>Control de plagas</b>\n\n"
        "• Broca del café: trampas con alcohol\n"
        "• Roya: fungicidas preventivos\n"
        "• Minador: podas sanitarias\n\n"
        "🔎 Monitoreo frecuente = prevención efectiva"
    )
}

# --- Funciones Mejoradas ---
def obtener_datos_region(region):
    regiones = {
        "antioquia": (
            "📍 <b>Datos para Antioquia</b>\n\n"
            "• pH promedio: 6.1\n"
            "• Humedad: 70%\n"
            "• Cultivos principales: café, aguacate\n\n"
            "🌡 <i>Temperatura promedio: 22°C</i>"
        ),
        "huila": (
            "📍 <b>Datos para Huila</b>\n\n"
            "• pH promedio: 6.3\n"
            "• Humedad: 65%\n"
            "• Cultivos principales: café, plátano\n\n"
            "🌡 <i>Temperatura promedio: 24°C</i>"
        ),
        "caldas": (
            "📍 <b>Datos para Caldas</b>\n\n"
            "• pH promedio: 6.2\n"
            "• Humedad: 75%\n"
            "• Cultivos principales: café, caña de azúcar\n\n"
            "🌡 <i>Temperatura promedio: 20°C</i>"
        ),
        "quindio": (
            "📍 <b>Datos para Quindío</b>\n\n"
            "• pH promedio: 6.0\n"
            "• Humedad: 72%\n"
            "• Cultivos principales: café, plátano\n\n"
            "🌡 <i>Temperatura promedio: 21°C</i>"
        ),
        "risaralda": (
            "📍 <b>Datos para Risaralda</b>\n\n"
            "• pH promedio: 6.1\n"
            "• Humedad: 73%\n"
            "• Cultivos principales: café, banano\n\n"
            "🌡 <i>Temperatura promedio: 22°C</i>"
        )
    }
    return regiones.get(region.lower(), "📌 Lo siento, aún no tengo datos para esa región.")

# --- Handlers Interactivos ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    hora = datetime.now().hour
    saludo = "¡Hola! ☕"  # Saludo cordial con emoticono de café

    
    keyboard = [
        [InlineKeyboardButton("🌱 Suelo", callback_data="suelo"),
         InlineKeyboardButton("🌤️ Clima", callback_data="clima")],
        [InlineKeyboardButton("🌿 Fertilizante", callback_data="fertilizante"),
         InlineKeyboardButton("🐛 Plagas", callback_data="plagas")],
        [InlineKeyboardButton("📊 Predicción", callback_data="prediccion")],
        [InlineKeyboardButton("☕ Cafés de Colombia", url="https://cafesdecolombia.co/informacion-sobre-cafe/"),
         InlineKeyboardButton("🌦️ IDEAM", url="https://www.ideam.gov.co/"),
         InlineKeyboardButton("🔬 AGROSAVIA", url="https://www.agrosavia.co/")]
    ]

    
    await update.message.reply_text(
        f"{saludo} Soy **Prada IA**, tu asistente agrícola inteligente. 🌱\n\n"
        "Prada IA está diseñado para brindarte recomendaciones y predicciones personalizadas sobre el cultivo de café. "
        "Con la ayuda de datos históricos y específicos de tu región, te ayudo a mejorar el rendimiento de tus cultivos, "
        "proporcionándote información sobre el suelo, clima, fertilización y control de plagas. 📊🌾\n\n"
        "¿Sobre qué tema necesitas ayuda hoy?",
        reply_markup=InlineKeyboardMarkup(keyboard)

    )
        
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data in respuestas:
        await query.edit_message_text(
            text=respuestas[query.data],
            parse_mode='HTML')
    elif query.data == "prediccion":
        await query.edit_message_text(
            text="🔍 <b>Predicción de Rendimiento</b>\n\n"
                 "Envía el pH y cantidad de fertilizante en este formato:\n"
                 "<code>predicción 5.8 25</code>",
            parse_mode='HTML')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    
    if "predicción" in texto:
        try:
            _, ph, fert = texto.split()
            respuesta = predecir_rendimiento(float(ph), float(fert))
        except:
            respuesta = "❗ Usa: <code>predicción &lt;pH&gt; &lt;fertilizante&gt;</code>\nEjemplo: predicción 6.2 25"
    elif any(region in texto for region in ["antioquia", "huila", "caldas", "quindio", "risaralda"]):
        # Aquí corregimos para verificar correctamente todas las regiones
        if "antioquia" in texto:
            region = "antioquia"
        elif "huila" in texto:
            region = "huila"
        elif "caldas" in texto:
            region = "caldas"
        elif "quindio" in texto:
            region = "quindio"
        elif "risaralda" in texto:
            region = "risaralda"
        respuesta = obtener_datos_region(region)
    elif any(keyword in texto for keyword in respuestas):
        keyword = next(key for key in respuestas.keys() if key in texto)
        respuesta = respuestas[keyword]
    else:
        respuesta = (
            "🤖 No entendí tu consulta. Prueba con:\n\n"
            "• <b>Suelo</b>: características ideales\n"
            "• <b>Clima</b>: condiciones óptimas\n"
            "• <b>Fertilizante</b>: recomendaciones\n"
            "• <b>Plagas</b>: control de enfermedades\n"
            "• <b>Predicción 6.2 25</b>: estimación de rendimiento"
        )
    
    await update.message.reply_text(respuesta, parse_mode='HTML')

# --- Imágenes y Comandos ---
async def enviar_imagen(update: Update, context: ContextTypes.DEFAULT_TYPE, imagen: str, caption: str):
    try:
        with open(f"imagenes/{imagen}", "rb") as img:
            await update.message.reply_photo(img, caption=caption)
    except Exception as e:
        await update.message.reply_text(f"⚠️ No pude cargar la imagen. Error: {e}")

# Función para enviar imagen de cafe
async def enviar_imagen_cafe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enviar_imagen(update, context, "suelo.jpeg", "🌱 Suelo ideal para café")

# Función para enviar imagen de clima
async def enviar_imagen_clima(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enviar_imagen(update, context, "clima.jpeg", "🌤️ Clima adecuado para cultivo")

# Función para enviar imagen de plaga
async def enviar_imagen_plaga(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enviar_imagen(update, context, "plaga.jpeg", "🐛 Plagas comunes del café")

# Función para enviar imagen de fertilizante
async def enviar_imagen_fertilizante(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await enviar_imagen(update, context, "fertilizante.jpg", "🌿 Plan de fertilización para café")

# --- Inicialización del Bot ---
if __name__ == "__main__":
    app = ApplicationBuilder().token("8076396530:AAGCVmQ0aCEdOivp17Ec3v2HzIkB0xcB8Tw").build()
    
    # Handlers principales
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Handlers de imágenes
    app.add_handler(CommandHandler("suelo_img", enviar_imagen_cafe))
    app.add_handler(CommandHandler("clima_img", enviar_imagen_clima))
    app.add_handler(CommandHandler("plaga_img", enviar_imagen_plaga))  # Handler para imagen de plaga
    app.add_handler(CommandHandler("fertilizante_img", enviar_imagen_fertilizante))  # Handler para imagen de fertilizante
    
    print("🤖 Bot agrícola en funcionamiento...")
    app.run_polling()


