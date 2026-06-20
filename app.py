from flask import Flask, jsonify, request
from flask_cors import CORS
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

ellas = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    description="Assistente da loja ELLAS DENIM, vende roupas jeans e sugere looks",
    markdown=True
)

toys = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    description="Assistente de loja de brinquedos, responde de forma divertida e simples",
    markdown=True
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    pergunta = data.get("pergunta")
    tipo = data.get("tipo")

    if tipo == "ellas":
        r = ellas.run(pergunta)
        return jsonify({"resposta": r.content})

    if tipo == "toys":
        r = toys.run(pergunta)
        return jsonify({"resposta": r.content})

    return jsonify({"erro": "tipo invalido"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)