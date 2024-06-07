from rank_bm25 import BM25Okapi
from pymongo import MongoClient
from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
from flask import Flask, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

client = MongoClient('mongodb://localhost:27017/')
db = client.projet
faq_collection = db.euro

faqs = list(faq_collection.find({}))
contexts = [faq['contexte'] for faq in faqs]
print(contexts)

nlp = pipeline('question-answering', model="deepset/roberta-base-squad2", tokenizer="deepset/roberta-base-squad2")
qa_t5 = pipeline("text2text-generation", model="google/flan-t5-xl")



def find_best_context(question, contexts):
    vectorizer = TfidfVectorizer().fit_transform(contexts + [question])
    vectors = vectorizer.toarray()
    question_vector = vectors[-1]
    context_vectors = vectors[:-1]
    similarities = cosine_similarity([question_vector], context_vectors)
    best_context_index = np.argmax(similarities)
    return contexts[best_context_index]


tokenized_contexts = [context.split(" ") for context in contexts]
bm25 = BM25Okapi(tokenized_contexts)
embedder = SentenceTransformer('paraphrase-MiniLM-L6-v2')


def find_best_context1(question, contexts):
    vectorizer = TfidfVectorizer().fit(contexts + [question])
    context_vectors = vectorizer.transform(contexts)
    question_vector = vectorizer.transform([question])

    similarities = cosine_similarity(question_vector, context_vectors).flatten()
    best_context_index = np.argmax(similarities)

    return contexts[best_context_index]

app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("text")
    if not user_input:
        return jsonify({"error": "Invalid input"}), 400

    best_context = find_best_context1(user_input, contexts)
    best_context1 = find_best_context(user_input, contexts)

    input_text = {
        'question': user_input,
        'context': best_context
    }

    result = nlp(input_text)

    response = {
        "input": input_text,
        "response": result if result else "Désolé, je ne peux pas répondre à cette question pour le moment.",
        "context": best_context
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
