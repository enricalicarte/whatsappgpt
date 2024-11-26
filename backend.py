from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Configura tu clave API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

# Contextos específicos por marca
assistant_contexts = {
    "Cumlaude": "Asistente experto en productos Cumlaude.",
    "Rilastil": "Asistente experto en productos Rilastil.",
    "Sensilis": "Asistente experto en productos Sensilis."
}

# IDs de los asistentes personalizados por marca
assistant_ids = {
    "Cumlaude": "asst_YvXWL3CSeZFLrIa9PrqLNBD2",
    "Rilastil": "asst_YLRcFQZNSosoKwMzzSMBHbL8",
    "Sensilis": "asst_Uc7dJy3DPCcsGkKyeqCRbCUc"
}

@app.route("/", methods=["GET"])
def home():
    return "¡Bienvenido al backend de WhatsAppGPT!", 200

@app.route("/ask", methods=["POST"])
def ask_gpt():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.get_json()
        prompt = data.get("prompt", "").strip()
        brand = data.get("brand", "").strip()

        if not prompt or not brand:
            return jsonify({"error": "Faltan 'prompt' o 'brand' en la solicitud"}), 400

        if brand not in assistant_ids:
            return jsonify({"error": f"Marca no válida: {brand}"}), 400

        # Seleccionar el ID del asistente basado en la marca
        assistant_id = assistant_ids[brand]

        # Configurar el mensaje de contexto
        system_message = {"role": "system", "content": assistant_contexts[brand]}

        # Llamar a la API de OpenAI
        response = openai.ChatCompletion.create(
            model=assistant_id,  # Usar el ID del asistente correspondiente
            messages=[
                system_message,
                {"role": "user", "content": prompt}
            ]
        )

        # Extraer la respuesta del asistente
        assistant_response = response["choices"][0]["message"]["content"]
        return jsonify({"response": assistant_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
