import logging
logging.getLogger("torch").setLevel(logging.ERROR)
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import re
MODEL_PATH = "./llama-intent"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    dtype=torch.float16,
    device_map="auto"
)

print("Modelo cargado")


INTENCIONES_VALIDAS = [
    "AGENDAR_MEET",
    "SOLICITAR_CV",
    "OTRA",
]



def clasificar(mensaje):
    messages = [
        {
            "role": "system",
            "content": (
                "Clasifica el mensaje del usuario en exactamente una de estas "
                "intenciones: AGENDAR_MEET, SOLICITAR_CV u OTRA. "
                "AGENDAR_MEET: el usuario quiere agendar o coordinar una "
                "llamada o videollamada. "
                "SOLICITAR_CV: el usuario quiere recibir, ver o descargar "
                "el CV. "
                "OTRA: cualquier otro mensaje que no requiera esas dos acciones. "
                "Responde únicamente con la etiqueta, sin explicaciones."
            )
        },
        {
            "role": "user",
            "content": mensaje
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    ).to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=10,
            do_sample=False
        )

    respuesta = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[1]:],
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    ).strip()

    # Exactamente una etiqueta
    if respuesta in INTENCIONES_VALIDAS:
        return respuesta

    # Buscar una etiqueta válida dentro de la respuesta
    for intencion in INTENCIONES_VALIDAS:

        patron = rf"\b{re.escape(intencion)}\b"

        if re.search(patron, respuesta):
            print(
                f"⚠️ Se corrigió salida: "
                f"{respuesta!r} -> {intencion}"
            )

            return intencion

    # Nada reconocible
    print(
        f"❌ Salida no válida: {respuesta!r}"
    )

    return "OTRA"
 
preguntas={
"AGENDAR_MEET" : [

    # =========================
    # AGENDAR_MEET
    # =========================
    "¿Podemos hacer un Meet para hablar de tu experiencia?",
    "¿Me puedes mandar un link de Meet?",
    "¿Cuándo tienes disponibilidad para una llamada?",
    "¿Podemos hablar mañana?",
    "¿Tienes tiempo para una videollamada?",
    "Me gustaría platicar contigo por videollamada",
    "¿Te parece si hacemos una llamada el viernes?",
    "¿A qué hora podemos hacer una llamada?",
    "¿Podemos tener una reunión por Meet?",
    "Agendamos una llamada para mañana",
    "¿Me compartes tu disponibilidad?",
    "¿Podemos coordinar una reunión?",
    "Quiero hablar contigo por Google Meet",
    "¿Te queda bien una llamada en la tarde?",
    "¿Podemos vernos en una videollamada?",
    "Avísame qué día te funciona para una llamada",
    "¿Qué horario tienes disponible?",
    "¿Podemos hablar unos minutos por Meet?",
    "¿Te parece si agendamos una videollamada?",
    "Necesito coordinar una llamada contigo",
    "¿Hacemos una reunión esta semana?",

    # Formas más indirectas
    "Me gustaría conversar contigo en persona",
    "¿Podemos platicar un rato?",
    "¿Tendrías unos minutos para hablar?",
    "Quisiera comentarte algo en una llamada",
    "¿Te puedo marcar?",
    "¿Podemos hablar por videollamada el jueves?",
    "Cuando tengas tiempo me gustaría hablar contigo",
    "¿Cuándo podríamos conversar?",
    "¿Te parece bien hablar mañana a las 5?",

    # Errores / escritura informal
    "podemos hacer una yamada?",
    "cuando podemos hacer un meet",
    "tienes tienpo para una videollamada?",
    "podemos platicar por meet mañana",
    "cuando te puedo marcar",
    "nos echamos un meet?",
    "agendamos una llamada?",
    "que orario tienes disponible?",
    "Cuando tengas tiempo hablamos",
    "¿Cuándo podemos hablar de la vacante?",
 "¿Me compartes tu perfil y luego coordinamos una llamada?",
 "Me interesa tu perfil, ¿podemos hablar?",
 "¿Podemos reunirnos para revisar tu experiencia?",

  "que onda, cuando podemos hablar?",
  "me interesa tu perfil, cuando tienes tiempo?",
    
],
"SOLICITAR_CV":[

    # =========================
    # SOLICITAR_CV
    # =========================
      "hola, me puedes compartir tu curriculum porfa",
    "¿Me puedes enviar tu CV?",
    "¿Me compartes tu currículum?",
    "¿Podrías mandarme tu currículum vitae?",
    "Quiero ver tu CV",
    "¿Dónde puedo descargar tu CV?",
    "¿Tienes tu CV disponible?",
    "¿Me pasas tu CV?",
    "¿Podrías compartirme tu CV?",
    "¿Me envías tu currículum por favor?",
    "Necesito tu CV",
    "¿Puedes compartir tu hoja de vida?",
    "¿Tienes un currículum que me puedas mandar?",
    "¿Me podrías hacer llegar tu CV?",
    "¿Me mandas tu currículum?",
    "Quisiera revisar tu CV",
    "¿Dónde veo tu currículum?",
    "Me interesa ver tu perfil, ¿me compartes tu CV?",
    "¿Puedes hacerme llegar tu currículum?",
    "¿Me puedes proporcionar tu CV?",
    "¿Tendrás tu CV en PDF?",

    # Formas indirectas
    
    "¿Tienes algún documento con tu experiencia?",

   
    "¿Tienes algún archivo con tu información profesional?",

    # Errores / informal
    "me puedes mandar tu cv",
    "me pasas el cv",
    "mandame tu curriculum",
    "me compartes tu curriculm",
    "tienes tu cv?",
    "me mandas tu hoja de vida?",
    "puedes pasarme el cv?",
    "¿Me mandas tu CV para revisarlo antes de la llamada?",
    "Quiero conocer tu experiencia, ¿me mandas tu CV?",
     "oye me pasas tu cv pls",
 "hola, tendras tu cv por ahi?",
   "bro me pasas tu cv",
   "Mándame tu CV cuando puedas",

],
"OTRA":[
    # =========================
    # OTRA
    # =========================
"Quisiera conocer más de tu experiencia profesional",
"¿Me compartes información sobre tu trayectoria?",
"¿Dónde puedo consultar tu experiencia?",
    "Hola",
    "Hola, buenos días",
    "Buenas tardes",
    "¿Cómo estás?",
    "Muchas gracias",
    "Gracias por la información",
    "Perfecto",
    "Excelente",
    "Ok",
    "Va",
    "Entendido",
    "De acuerdo",
    "Nos vemos",
    "Saludos",

    # Preguntas sobre experiencia
    "¿Qué experiencia tienes con Python?",
    "¿Cuántos años llevas programando?",
    "¿Has trabajado con Java?",
    "¿Qué proyectos has realizado?",
    "¿Qué tecnologías manejas?",
    "¿Tienes experiencia con bases de datos?",
    "Cuéntame sobre tu experiencia",
    "¿En qué empresas has trabajado?",
    "¿Qué tipo de proyectos has desarrollado?",
    "¿Has trabajado con AWS?",

    # Preguntas laborales que no solicitan CV
    "¿Cuál es tu expectativa salarial?",
    "¿Actualmente estás trabajando?",
    "¿Por qué quieres cambiar de empleo?",
    "¿Estás disponible para trabajar?",
    "¿Buscas trabajo actualmente?",
    "¿Te interesa la vacante?",
    "¿Cuándo podrías comenzar?",
    "¿Tienes disponibilidad inmediata?",
    "¿La vacante es remota?",
    "¿Dónde están las oficinas?",

    # Conversación general
    "Me interesa tu experiencia",
    "Cuéntame un poco de ti",
    "¿Qué haces actualmente?",
    "Platícame sobre ti",
    "Quiero conocerte un poco más",
    "¿Cómo fue tu último proyecto?",


    "hola",
    "ok",
    "gracias",

]

    
}
   
resultados={
     "AGENDAR_MEET":[0,0],
     "SOLICITAR_CV":[0,0],
     "OTRA":[0,0]
 }
for categoria in preguntas:
    for mensaje in preguntas[categoria]:
        respuesta= clasificar(mensaje)
    
        if respuesta == categoria:
            resultados[categoria][0]+=1
        else:
            resultados[categoria][1]+=1
            print(mensaje)
            print("→", respuesta)
print(resultados)
