from flask import Flask, request, Response
import openai
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Carga tu API Key de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # puedes cambiar a gpt-4 si tienes acceso
            messages=[
                {"role": "system", "content": "Eres Kai, el asistente de Kanguro GT. Ayudas a los clientes con sus dudas sobre sillas, pedidos y soporte."},
                {"role": "user", "content": mensaje}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "Hubo un error procesando tu mensaje. Intenta más tarde."

if __name__ == "__main__":
import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)
