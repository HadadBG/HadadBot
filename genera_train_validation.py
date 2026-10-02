import random
import json
data={
"AGENDAR_MEET": [
        "Hola, ¿podemos agendar una llamada?",
        "¿Cuándo tienes disponibilidad para una videollamada?",
        "Me gustaría platicar contigo por Meet.",
        "¿Podemos tener una entrevista esta semana?",
        "¿Te parece si hacemos una llamada para hablar de la vacante?",
        "Quisiera coordinar una reunión contigo.",
        "¿Podemos agendar una reunión por Google Meet?",
        "Me interesa hablar contigo en una llamada.",
        "¿Tienes algún horario disponible mañana para una llamada?",
        "¿Podemos vernos por videollamada?",
        "¿Qué día te funciona para una entrevista?",
        "¿Me compartes horarios para agendar una llamada?",
        "Quiero agendar una reunión contigo.",
        "¿Podemos hablar por Meet el jueves?",
        "¿Tienes espacio para una llamada de 30 minutos?",
        "Me gustaría coordinar una videollamada.",
        "¿Cuándo podemos tener una reunión?",
        "¿Te puedo poner una junta por Meet?",
        "¿Podemos hacer una llamada para conocernos?",
        "¿Tienes disponibilidad esta tarde para una videollamada?",
        "Quiero platicar contigo en una entrevista.",
        "¿Podríamos agendar una llamada la próxima semana?",
        "¿A qué hora te viene bien una reunión?",
        "¿Me puedes dar disponibilidad para un Meet?",
        "¿Podemos calendarizar una entrevista?",
        "¿Te parece una llamada mañana?",
        "Necesito agendar una reunión contigo.",
        "¿Podemos hablar por video?",
        "Me interesa coordinar una llamada para revisar la posición.",
        "¿Qué horario tienes libre para una videollamada?",
        "¿Podemos reservar media hora para hablar?",
        "¿Te funciona el viernes para una llamada?",
        "Me gustaría agendar algo contigo.",
        "¿Podemos hacer una reunión virtual?",
        "¿Tienes algún hueco para una entrevista?",
        "¿Podemos apartar un espacio para platicar?",
        "Quisiera agendar un Meet para conversar sobre la vacante.",
        "¿Me pasas tus horarios disponibles?",
        "¿Podemos agendarlo por Google Meet?",
        "¿Qué día puedes para una llamada?",
        "¿Te va bien una videollamada el miércoles?",
        "¿Hay manera de coordinar una entrevista?",
        "Me gustaría tener una llamada contigo.",
        "¿Podemos poner una reunión en calendario?",
        "¿Cuándo te queda bien un Meet?",
        "¿Podemos agendar una llamada de seguimiento?",
        "Necesito coordinar una videollamada contigo.",
        "¿Tienes disponibilidad el jueves a las 5?",
        "¿Podemos hablar por Meet esta semana?",
        "¿Me ayudas a agendar una entrevista?",
        "¿Qué horarios manejas para llamadas?",
        "Quisiera reservar un horario para hablar contigo.",
        "¿Podemos hacer una reunión virtual de 30 min?",
        "¿Qué hora te funciona mañana para un Meet?",
        "Me interesa una llamada para conocer más de la oportunidad.",
        "¿Te parece si coordinamos una entrevista?",
        "¿Podemos dejar agendada una llamada?",
        "¿Cuál es tu disponibilidad para el lunes?",
        "¿Agendamos una videollamada?",
        "¿Me puedes compartir un espacio para platicar por Meet?",
        "¿Te puedo marcar?",
    "¿Cuándo podemos conversar?",
    "Cuando tengas tiempo me gustaría hablar contigo",
    "Cuando tengas tiempo hablamos",
    "¿Cuándo podríamos platicar?",
    "¿Tienes un momento para hablar?",
    "¿Podemos hablar mañana?",
    "¿Te puedo llamar más tarde?",
    "¿Cuándo te puedo marcar?",
    "Me gustaría conversar contigo",
    "Me interesa tu perfil, ¿podemos hablar?",
    "Me interesa tu perfil, ¿cuando tienes tiempo?",
    "Quisiera platicar contigo un momento",
    "¿Podemos conversar esta semana?",
    "¿Te parece si hablamos mañana?",
    "¿Tendrías unos minutos para hablar?",
    "¿Podemos platicar un rato?",
    "Cuando tengas oportunidad hablamos",
    "Avísame cuando puedas hablar",
    "¿En qué momento podemos hablar?",
    "¿Te parece bien que hablemos mañana?",
    "Quisiera hablar contigo sobre la vacante",
    "Me gustaría comentarte algo por llamada",
    "¿Podemos conversar sobre la posición?",
    "¿Te marco en la tarde?",
    "¿A qué hora te puedo llamar?",
    "¿Tienes unos minutos para platicar?",
    "¿Podemos hablar un momento sobre la vacante?",
    "Quiero platicar contigo sobre el puesto",
    "¿Podemos coordinar un momento para hablar?",
     "te puedo marcar?",
    "cuando te puedo llamar?",
    "podemos platicar mañana?",
    "cuando podemos ablar?",
    "tienes tienpo para hablar?",
    "cuando podemos platicar?",
    "nos echamos un meet?",
    "podemos aser una llamada?",
       "¿Te puedo marcar?",
    "¿Cuándo podemos conversar?",
    "Cuando tengas tiempo me gustaría hablar contigo",
    "Cuando tengas tiempo hablamos",
    "¿Cuándo podríamos platicar?",
    "¿Tienes un momento para hablar?",
    "¿Podemos hablar mañana?",
    "¿Te puedo llamar más tarde?",
    "¿Cuándo te puedo marcar?",
    "Me gustaría conversar contigo",
    "Me interesa tu perfil, ¿podemos hablar?",
    "Me interesa tu perfil, ¿cuando tienes tiempo?",
    "Quisiera platicar contigo un momento",
    "¿Podemos conversar esta semana?",
    "¿Te parece si hablamos mañana?",
    "¿Tendrías unos minutos para hablar?",
    "¿Podemos platicar un rato?",
    "Cuando tengas oportunidad hablamos",
    "Avísame cuando puedas hablar",
    "¿En qué momento podemos hablar?",
    "¿Te parece bien que hablemos mañana?",
    "Quisiera hablar contigo sobre la vacante",
    "¿Podemos conversar sobre la posición?",
    "¿Te marco en la tarde?",
    "¿A qué hora te puedo llamar?",
    "¿Tienes unos minutos para platicar?",
    "¿Podemos hablar un momento sobre la vacante?",
    "Quiero platicar contigo sobre el puesto",
       "¿Te puedo marcar?",
    "¿Te puedo llamar?",
    "¿Puedo marcarte?",
    "¿Puedo llamarte?",
    "¿Te marco?",
    "¿Te llamo?",
    "¿Te puedo marcar más tarde?",
    "¿Te puedo marcar mañana?",
    "¿Puedo marcarte por teléfono?",
    "¿Te puedo contactar por llamada?",
    "¿Cuándo te puedo marcar?",
    "¿A qué hora te puedo marcar?",
    "¿Te marco en un rato?",
    "¿Te llamo en la tarde?",
    "¿Puedo llamarte esta semana?"
    ],
    "SOLICITAR_CV": [
        "Hola, ¿me puedes compartir tu CV?",
        "¿Me mandas tu currículum?",
        "¿Tienes tu CV para enviármelo?",
        "¿Me podrías pasar tu currículum vitae?",
        "¿Me compartes tu CV por favor?",
        "Quisiera recibir tu currículum.",
        "¿Me envías tu CV?",
        "¿Tendrás tu CV actualizado?",
        "¿Me puedes hacer llegar tu CV?",
        "¿Puedes mandarme tu hoja de vida?",
        "¿Me pasas el CV que usaste para aplicar?",
        "¿Nos compartes tu currículum?",
        "¿Podrías enviarme tu CV en PDF?",
        "¿Me mandas tu CV por aquí?",
        "¿Tienes disponible tu currículum?",
        "¿Podrías compartir tu perfil en CV?",
        "¿Me envías tu documento de CV?",
        "¿Me puedes pasar tu currículum actualizado?",
        "¿Tendrás el archivo de tu CV?",
        "¿Me compartes el documento con tu experiencia?",
        "¿Puedes hacerme llegar tu CV, por favor?",
        "¿Me mandas el currículum que tienes actualmente?",
        "¿Me podrías enviar tu CV?",
        "¿Me pasas tu hoja de vida?",
        "¿Tienes un CV que me puedas compartir?",
        "¿Me envías tu currículum vitae?",
        "¿Puedes compartir tu CV conmigo?",
        "¿Me puedes mandar el archivo de tu currículum?",
        "¿Me compartes tu CV para revisarlo?",
        "¿Podrías mandarme tu currículum por WhatsApp?",
        "¿Me haces llegar tu CV?",
        "¿Dónde puedo ver o descargar tu CV?",
        "¿Me pasas tu CV, porfa?",
        "Me interesa tu perfil, ¿me compartes tu CV?",
        "¿Podrías enviarme tu CV en formato PDF?",
        "¿Me mandas el CV que tienes?",
        "¿Me compartes tu currículum por este medio?",
        "¿Puedes enviarme tu CV actualizado?",
        "¿Me ayudas compartiendo tu CV?",
        "¿Me podrías pasar tu CV para el proceso?",
        "¿Nos puedes enviar tu currículum?",
        "¿Me mandas tu perfil profesional en CV?",
        "¿Me compartes tu CV para la vacante?",
        "¿Tendrías manera de enviarme tu CV?",
        "¿Me pasas tu currículum para conocer tu trayectoria?",
        "¿Puedes mandarme tu CV en PDF?",
        "¿Me compartes el archivo de tu CV?",
        "¿Me envías tu CV por favor?",
        "¿Me podrías mandar tu hoja de vida?",
        "¿Tienes tu CV a la mano?",
        "¿Me compartes la versión más reciente de tu CV?",
        "¿Puedes enviarme tu currículum actualizado?",
        "¿Me mandas tu CV para revisarlo?",
        "¿Podrías hacerme llegar tu currículum?",
        "¿Me pasas tu CV por aquí?",
        "¿Me puedes proporcionar tu CV?",
        "¿Sería posible que me enviaras tu currículum?",
        "¿Me compartes tu CV, gracias?",
        "Necesito tu CV para continuar con el proceso.",
          "me compartes tu curriculm",
    "me pasas tu curriculm",
    "me mandas tu curriclum",
    "me compartes tu curriclum",
    "me pasas tu curiculum",
    "me mandas tu curiculum",
    "me compartes tu curriculun",
    "me mandas tu curriculun",
    "me pasas el curriculo",
    "me compartes el curriculo",
    "me mandas el cv",
    "me pasas el cv porfa",
    "me puedes mandar el cv?",
    "m puedes compartir tu cv?",
    "me compartes tu hoja de vida?",
    
    ],
   "OTRA": [
    # Disponibilidad laboral
    "¿Estás disponible para trabajar?",
    "¿Tienes disponibilidad inmediata?",
    "¿Cuándo podrías comenzar?",
    "¿Cuándo podrías incorporarte?",
    "¿Tienes disponibilidad para la vacante?",
    "¿Puedes empezar el lunes?",
    "¿Cuál es tu disponibilidad laboral?",
    "¿Actualmente estás disponible?",
    "¿Estás buscando trabajo actualmente?",
    "¿Cuándo estarías disponible para comenzar?",

    # Vacante
    "¿Te interesa la vacante?",
    "¿Te interesa el puesto?",
    "¿Qué opinas de la vacante?",
    "¿Te interesa esta oportunidad?",
    "¿Qué te parece la posición?",
    "¿Sigues interesado en la vacante?",
    "¿Te gustaría formar parte del equipo?",

    # Condiciones laborales
    "¿La vacante es remota?",
    "¿Dónde están las oficinas?",
    "¿Cuál es el horario de trabajo?",
    "¿Cuánto ofrecen de salario?",
    "¿Cuál es el sueldo?",
    "¿Qué prestaciones tienen?",
    "¿Es trabajo híbrido?",
    "¿Cuántos días se trabaja en oficina?",
    "¿Dónde está ubicada la empresa?",

    # Experiencia
    "¿Qué experiencia tienes con Python?",
    "¿Has trabajado con Java?",
    "¿Cuántos años llevas programando?",
    "¿Qué tecnologías manejas?",
    "¿Has trabajado con AWS?",
    "¿Qué proyectos has realizado?",
    "¿Cuál ha sido tu proyecto más importante?",
    "¿Cómo aprendiste a programar?",
    "¿Qué te gusta de Python?",

    # Conversación que NO necesariamente implica reunión
    "Cuéntame un poco de ti",
    "Platícame sobre tu experiencia",
    "Háblame sobre tus proyectos",
    "Quiero saber más sobre tu experiencia",
    "Me interesa tu experiencia",
    "Cuéntame cómo has trabajado con Python",
    "¿Qué haces actualmente?",
    "¿En qué has trabajado?",
    
    # Respuestas/conversación
    "Hola",
    "Buenos días",
    "Buenas tardes",
    "Gracias",
    "Muchas gracias",
    "Perfecto",
    "Ok",
    "Va",
    "Entendido",
    "De acuerdo",
    "Excelente",
    "Nos vemos",
    "Nos vemos luego",
    "Nos vemos mañana",
    "Hasta luego",
    "Hasta pronto",
    "Que tengas buen día",
    "Seguimos en contacto",
    "Estamos en contacto",
    
    # Ambiguos
    "Me interesa",
    "Quisiera conocerte mejor",
    "Platícame",
    "Cuéntame más",
    "Tengo una duda",
    "Quisiera preguntarte algo",
]
    }

SYSTEM = (
    "Clasifica el mensaje del usuario en exactamente una de estas intenciones: "
    "AGENDAR_MEET, SOLICITAR_CV u OTRA. "
    "AGENDAR_MEET: el usuario quiere agendar o coordinar una llamada o videollamada. "
    "SOLICITAR_CV: el usuario quiere recibir, ver o descargar el CV. "
    "OTRA: cualquier otro mensaje que no requiera esas dos acciones. "
    "Responde únicamente con la etiqueta, sin explicaciones."
)

'''
SYSTEM = (
    "Clasifica el mensaje del usuario en exactamente una de estas intenciones: "
    "AGENDAR_MEET, SOLICITAR_CV u OTRA. "

    "AGENDAR_MEET: el usuario quiere agendar, coordinar, confirmar o realizar "
    "una llamada, videollamada, reunión o conversación por teléfono/Meet. "
    "Debe existir una intención clara de hablar o reunirse. "

    "SOLICITAR_CV: el usuario quiere recibir, ver, descargar o compartir el CV, "
    "currículum o hoja de vida. "

    "OTRA: cualquier mensaje que no solicite una llamada/reunión/videollamada "
    "y que tampoco solicite el CV. Incluye preguntas sobre experiencia, salario, "
    "vacantes, disponibilidad laboral, inicio de trabajo, modalidad remota, "
    "ubicación de oficinas y cualquier otro tema laboral o conversación general. "

    "Importante: 'disponibilidad', 'tiempo', 'cuando puedes' o 'cuando podrías' "
    "NO significan AGENDAR_MEET por sí solos. Solo usa AGENDAR_MEET si el contexto "
    "indica claramente una llamada, reunión, videollamada o conversación. "

    "Responde únicamente con una de estas etiquetas: "
    "AGENDAR_MEET, SOLICITAR_CV u OTRA."
)
'''
prefixes = ["", "Hola, ", "Oye, ", "Disculpa, ", "Una pregunta: ", "Por cierto, "]
suffixes = ["", " por favor", " porfa", " pls", " 🙌", " 🙂", "?", " gracias"]


random.seed(42)


TRAIN_PER_CLASS = 350
VALIDATION_RATIO = 0.20

all_train = []
all_validation = []

for label, examples in data.items():

    # Eliminar duplicados originales
    examples = list(dict.fromkeys(
        ex.lower().strip() for ex in examples
    ))

    # Mezclar antes de hacer el split
    random.shuffle(examples)

    # Cantidad para validation
    validation_size = max(1, int(len(examples) * VALIDATION_RATIO))

    validation_examples = examples[:validation_size]
    train_examples = examples[validation_size:]

    # ---------------------------------------------------------
    # VALIDATION
    # Se quedan únicamente los ejemplos originales.
    # ---------------------------------------------------------
    for ex in validation_examples:
        all_validation.append({
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": ex},
                {"role": "assistant", "content": label},
            ]
        })

    # ---------------------------------------------------------
    # TRAIN
    # Primero metemos los ejemplos originales.
    # ---------------------------------------------------------
    generated = []
    seen = set()

    for ex in train_examples:
        generated.append({
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": ex},
                {"role": "assistant", "content": label},
            ]
        })

        seen.add(ex)

    # Guardamos los textos de validation para evitar
    # generar accidentalmente exactamente el mismo texto.
    validation_seen = set(validation_examples)

    # ---------------------------------------------------------
    # GENERAR VARIACIONES SOLO DEL TRAIN
    # ---------------------------------------------------------
    while len(generated) < TRAIN_PER_CLASS:

        ex = random.choice(train_examples)
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)

        v = " ".join((prefix + ex + suffix).split())

        # Corregir algunas cosas sencillas
        v = v.replace("??", "?")
        v = v.replace("!!", "!")

        key = v.lower().strip()

        # Evitar duplicados dentro de train
        # y coincidencias exactas con validation
        if key in seen:
            continue

        if key in validation_seen:
            continue

        seen.add(key)

        generated.append({
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": v},
                {"role": "assistant", "content": label},
            ]
        })

    all_train.extend(generated)


# Mezclar los datasets completos
random.shuffle(all_train)
random.shuffle(all_validation)

print("Train:", len(all_train))
print("Validation:", len(all_validation))

with open("train.jsonl", "w", encoding="utf-8") as f:
    for item in all_train:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

with open("validation.jsonl", "w", encoding="utf-8") as f:
    for item in all_validation:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")