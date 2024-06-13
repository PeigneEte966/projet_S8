from pymongo import MongoClient
from transformers import pipeline
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import torch
from werkzeug.exceptions import BadRequest

# Vérifier si le GPU est disponible et spécifier l'appareil
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Initialiser les pipelines NLP optimisés pour le français sur le GPU
qa = pipeline('question-answering', model='etalab-ia/camembert-base-squadFR-fquad-piaf', tokenizer='etalab-ia/camembert-base-squadFR-fquad-piaf', device=0 if device == 'cuda' else -1)

# Configuration de MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.projet
faq_collection = db.euro

def get_contexts_from_db():
    faqs = list(faq_collection.find({}))
    return [faq['contexte'] for faq in faqs]

def find_best_context(question, contexts):
    vectorizer = TfidfVectorizer().fit_transform(contexts + [question])
    vectors = vectorizer.toarray()
    question_vector = vectors[-1]
    context_vectors = vectors[:-1]
    similarities = cosine_similarity([question_vector], context_vectors).flatten()
    best_context_index = np.argmax(similarities)
    return contexts[best_context_index]

app = Flask(__name__)
#Permet d'ajouter une limite sur le nombre de requêtes faites par chaque utilisateur
limiter = Limiter(app, key_func=lambda: request.remote_addr)
CORS(app)
@app.route('/chat', methods=['POST'])
@limiter.limit('10 per minute')
def chat():
    try:
        # Check l'entrée pour éviter les injections SQL, script et autre attaques basée sur l'entrée
        json_data = request.get_json()
        if not json_data:
            raise BadRequest('Invalid input')

        user_input = request.json.get("text")
        print(user_input)
        if not user_input:
            return jsonify({"error": "Invalid input"}), 400

        contexts = get_contexts_from_db()
        best_context = find_best_context(user_input, contexts)

        input_text = {
            'question': user_input,
            'context': best_context
        }

        result = qa(input_text)
        print(result['answer'])
        print(best_context)
        response = {
            "response": best_context if result else "Désolé, je ne peux pas répondre à cette question pour le moment.",
        }

        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)