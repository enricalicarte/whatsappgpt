from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Configurar la clave API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)

# Asistentes asociados a cada marca
assistant_ids = {
    "Cumlaude": "asst_YvXWL3CSeZFLrIa9PrqLNBD2",
    # "Rilastil": "asst_YvXWL3CSeZFLrIa9PrqLNBD3",  # Comentado temporalmente
    # "Sensilis": "asst_YvXWL3CSeZFLrIa9PrqLNBD4"   # Comentado temporalmente
}

@app.route("/", methods=["GET"])
def home():
    return "¡Bienvenido al backend de WhatsAppGPT!", 200

@app.route("/ask", methods=["POST"])
def ask_openai():
    try:
        # Obtener datos del frontend
        data = request.get_json()
        prompt = data.get("prompt", "").strip()
        brand = data.get("brand", "Cumlaude").strip()

        if not prompt or brand not in assistant_ids:
            return jsonify({"error": "Datos de solicitud inválidos"}), 400

        # Usar el asistente asociado a la marca seleccionada
        assistant_id = assistant_ids[brand]
        print(f"Usando asistente: {assistant_id} para la marca {brand}")

        # Realizar la consulta a OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Cambia el modelo si es necesario
            messages=[{"role": "user", "content": prompt}],
            functions=None,
            function_call="none",
            assistant_id=assistant_id
        )

        # Devolver la respuesta al frontend
        return jsonify({"response": response.choices[0].message["content"]})

    except Exception as e:
        print(f"Error en el backend: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
