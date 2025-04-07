from flask import Flask, request, Response
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# Inicializa el cliente de OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cargar base de conocimiento local
with open("knowledge_base.txt", "r", encoding="utf-8") as f:
    KNOWLEDGE_BASE = f.read()

@app.route("/webhook", methods=["POST"])
def webhook():
    mensaje_usuario = request.form.get("Body")
    numero_usuario = request.form.get("From")

    respuesta = responder_con_kai(mensaje_usuario)

    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{respuesta}</Message>
</Response>"""

    return Response(xml_response, mimetype="text/xml")

def responder_con_kai(mensaje):
    try:
        system_prompt = f"""Responde únicamente con base en la siguiente información interna de procesos de la empresa:

{KNOWLEDGE_BASE}
"""
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": mensaje}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ ERROR: {e}", flush=True)
        return "Hubo un error procesando tu mensaje. Intenta más tarde."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)