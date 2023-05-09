from flask import Flask,request,jsonify  # Ajouter la bibliothèque request pour récupérer les données POST
from flask_cors import CORS
import hashlib  # Ajouter la bibliothèque hashlib pour hasher le mot de passe
from jwt_utils import build_token,decode_token,JwtError
from questions import Question

app = Flask(__name__)
CORS(app)

password_hash = 'd8170650479293c12e0201e5fdf45f40'  # Remplacer cette valeur par le vrai hash du mot de passe


@app.route('/')
def hello_world():
    x = 'world'
    return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def GetLogin():
    payload = request.get_json()  # Récupérer les données POST envoyées par le client
    tried_password = payload['password'].encode('UTF-8')
    hashed = hashlib.md5(tried_password).hexdigest()
    if hashed == password_hash:
        token = build_token()
        return {'token': token}, 200  # Retourner le token dans la réponse en JSON
    else:
        return {'error': 'Unauthorized'}, 401  # Retourner une erreur 401 Unauthorized si le mot de passe est incorrect



@app.route('/questions', methods=['POST'])
def create_question():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401

    question = Question(position=request.json['position'],
                        title=request.json['title'],
                        text=request.json['text'],
                        image=request.json['image'])
    question.save()

    return jsonify({'id': question.id}), 200




@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):

    question = Question.get_by_id(question_id)
    if question is None:
        return jsonify({'error': 'Question not found'}), 404
    return jsonify({'id': question.id,
                    'position': question.position,
                    'title': question.title,
                    'text': question.text,
                    'image': question.image}), 200

@app.route('/questions/position/<int:position>', methods=['GET'])
def get_question_by_position(position):
    question = Question.get_by_position(position)
    if question is None:
        return jsonify({'error': 'Question not found'}), 404
    return jsonify({'id': question.id,
                    'position': question.position,
                    'title': question.title,
                    'text': question.text,
                    'image': question.image}), 200


if __name__ == "__main__":
    app.run()
