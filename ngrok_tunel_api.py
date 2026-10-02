import os
from dotenv import load_dotenv
import re
from fastapi import FastAPI, Request, BackgroundTasks
import requests
import ollama
from pyngrok import ngrok
import uvicorn

load_dotenv()


PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
NGROK_AUTH_TOKEN=os.getenv("NGROK_AUTH_TOKEN")
ACCESS_TOKEN=os.getenv("ACCESS_TOKEN")
WHATSAPP_ACCESS_TOKEN=os.getenv("WHATSAPP_ACCESS_TOKEN")


INTENCIONES_VALIDAS = [
    "AGENDAR_MEET",
    "SOLICITAR_CV",
    "OTRA",
]
mensajes_recibidos = []
usuarios_conocidos = set()
MODEL_NAME = "llama-intent:latest"
def clasificar(mensaje):

    respuesta = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": mensaje
            }
        ],
        options={
            "temperature": 0,
            "num_predict": 10
        }
    )

    texto = respuesta["message"]["content"].strip()


    # Salida exacta
    if texto in INTENCIONES_VALIDAS:
        return texto


    # Buscar etiqueta válida
    for intencion in INTENCIONES_VALIDAS:

        patron = rf"\b{re.escape(intencion)}\b"

        if re.search(patron, texto):

            print(
                f"⚠️ Se corrigió salida: "
                f"{texto!r} -> {intencion}"
            )

            return intencion


    print(f"❌ Salida no válida: {texto!r}")

    return "OTRA"

horarios_diponibles=[
    "Lunes 10:00-11:00",
    "Lunes 11:00-12:00",
    "Lunes 12:00-13:00",
    "Lunes 13:00-14:00",
    "Lunes 14:00-15:00",
    "Lunes 15:00-16:00",
    "Lunes 17:00-18:00",
    "Jueves 10:00-11:00",
    "Jueves 11:00-12:00",
    "Jueves 12:00-13:00",
    "Jueves 13:00-14:00",
    "Jueves 14:00-15:00",
    "Jueves 15:00-16:00",
    "Jueves 17:00-18:00",
    ]

def normalizar_numero_mx(numero):
    if numero.startswith("521") and len(numero) == 13:
        return "52" + numero[3:]
    return numero

# Definir función de envío de respuesta
def enviar_respuesta(numero, texto):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {
            "body": texto
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30
    )

    print("STATUS META:", response.status_code)
    print("RESPUESTA META:", response.text)

    response.raise_for_status()


def procesar_y_responder(numero, texto):
    if numero not in usuarios_conocidos:
        usuarios_conocidos.add(numero)
        
        enviar_respuesta(numero, "¡Hola! Soy HadadBot🤖 El asistente personal de Hadad y estare encantado de recibir tus peticiónes, actualmente puedo entender solicitudes de cv o agendar citas.")

    intencion=clasificar(texto)
    if intencion == "AGENDAR_MEET":
         enviar_respuesta(numero,"Te comparto los horarios disponibles\n"+
                          "\n".join(horarios_diponibles)+
                          "\n En cuanto pueda Hadad personalmente agendara tu cita."
       )
    elif intencion == "SOLICITAR_CV":
        enviar_respuesta(numero,'''Claro, su cv lo puedes encontrar en la siguiente liga:
        https://hadadbg.github.io/documents/CV_Hadad_Bautista_Garcia.pdf''')
    else:
         enviar_respuesta(numero,"No entendi correctamente tu solicitud , podrias intentar de nuevo o en cuanto Hadad pueda te contestara personalmente")


app = FastAPI()


# Definir endpoint de verificación de credenciales
@app.get("/webhook")
async def verificar_webhook(request: Request):
    params = request.query_params
    if params.get("hub.verify_token") == ACCESS_TOKEN:
        return int(params.get("hub.challenge"))
    return {"error": "token invalido"}

@app.post("/webhook")
async def recibir_mensaje(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    mensajes_recibidos.append(body)
    try:
        mensaje = body["entry"][0]["changes"][0]["value"]["messages"][0]
        numero = normalizar_numero_mx(mensaje["from"])
        texto = mensaje["text"]["body"]
        background_tasks.add_task(procesar_y_responder, numero, texto)
    except (KeyError, IndexError):
        pass
    return {"status": "ok"}  # Meta recibe el ACK de inmediato, sin esperar a Ollama

ngrok.set_auth_token(NGROK_AUTH_TOKEN)
tunel_publico = ngrok.connect(8000)
print("URL a configurar como Callback URL en el dashboard de Meta:")
print(tunel_publico.public_url + "/webhook")
uvicorn.run(app, host="0.0.0.0", port=8000)


  