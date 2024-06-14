from pymongo import MongoClient
from transformers import pipeline
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sentence_transformers import SentenceTransformer, util
from werkzeug.exceptions import BadRequest
import numpy as np
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'

sentence_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2', device=device)

client = MongoClient('mongodb://localhost:27017/')
db = client.projet
faq_collection = db.euro
pouce_collection = db.pouce
suggestion_collection = db.suggestion

def get_contexts_from_db():
    faqs = list(faq_collection.find({}))
    return [faq['contexte'] for faq in faqs]

def find_best_context(question, contexts):
    question_embedding = sentence_model.encode(question, convert_to_tensor=True)
    context_embeddings = sentence_model.encode(contexts, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(question_embedding, context_embeddings)
    best_context_index = torch.argmax(similarities)
    return contexts[best_context_index]

app = Flask(__name__)
CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

@app.route('/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    try:
        json_data = request.get_json()
        if not json_data:
            raise BadRequest('Invalid input')
        
        user_input = json_data.get("text")
        if not user_input:
            return jsonify({"error": "Invalid input"}), 400

        contexts = get_contexts_from_db()
        best_context = find_best_context(user_input, contexts)

        input_text = {
            'question': user_input,
            'context': best_context
        }

        response = {
            "response": best_context if best_context else "Désolé, je ne peux pas répondre à cette question pour le moment.",
        }

        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/pouce', methods=['POST'])
@limiter.limit("10 per minute")
def pouce():
    try:
        json_data = request.get_json()
        if not json_data:
            raise BadRequest('Invalid input')
        
        user_input = json_data.get("pouce")
        message = user_input.get('message')
        reponse = user_input.get('reponse')
        
        if not message or not reponse:
            return jsonify({"error": "Invalid input"}), 400

        pouce_collection.insert_one({
            "message": message,
            "reponse": reponse
        })

        response = {
            "response": "pouce reçu",
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/suggestion', methods=['POST'])
@limiter.limit("10 per minute")
def suggestion():
    try:
        json_data = request.get_json()
        if not json_data:
            raise BadRequest('Invalid input')
        
        suggestion_text = json_data.get("suggestion")
        if not suggestion_text:
            return jsonify({"error": "Invalid input"}), 400

        suggestion_collection.insert_one({
            "suggestion": suggestion_text
        })

        response = {
            "response": "suggestion reçue",
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
