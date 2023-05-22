import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
from jwt_utils import build_token, decode_token, JwtError
from questions import Question, Answer, Participation, Score
import json

app = Flask(__name__)
CORS(app)

password_hash = 'd8170650479293c12e0201e5fdf45f40'

@app.route('/')
def hello_world():
    x = 'world'
    return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def get_quiz_info():
    return {"size":len(Question.get_all()) , "scores": []}, 200
 

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    tried_password = payload['password'].encode('UTF-8')
    hashed = hashlib.md5(tried_password).hexdigest()
    if hashed == password_hash:
        token = build_token()
        return {'token': token}, 200
    else:
        return {'error': 'Unauthorized'}, 401
    




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

    
    data = request.get_json()
    new_position = data['position']

    # Adjust positions if there is an existing question at the same position
    existing_question = Question.get_by_position(new_position)
    if existing_question:
        new_position = existing_question.position
        existing_question.position+=1
        existing_question.update()

        for q in Question.get_all():
            if q.id != existing_question.id and q.position >= new_position:
                q.position += 1
                q.update()
        

    question = Question(
        position=new_position,
        title=data['title'],
        text=data['text'],
        image=data['image'],
        possibleAnswers=json.dumps(data['possibleAnswers'])
    )
    question.save()

    if 'possibleAnswers' in data:
        for answer_data in data['possibleAnswers']:
            answer = Answer(
                question_id=question.id,
                text=answer_data['text'],
                is_correct=answer_data['isCorrect']
            )
            answer.save()

    return jsonify({'id': question.id}), 200







@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question(question_id):
    question = Question.get_by_id(question_id)
    if question is None:
        return jsonify({'error': 'Question not found'}), 404
    

    return jsonify({
        'id': question.id,
        'position': question.position,
        'title': question.title,
        'text': question.text,
        'image': question.image,
        'possibleAnswers': json.loads(question.possibleAnswers)
    }), 200

@app.route('/questions', methods=['GET'])
def get_question_by_position():
    position = request.args.get('position')
    question = Question.get_by_position(position)
    if question is None:
        return jsonify({'error': 'Question not found'}), 404


    
    return jsonify({
        'id': question.id,
        'position': question.position,
        'title': question.title,
        'text': question.text,
        'image': question.image,
        'possibleAnswers': json.loads(question.possibleAnswers)
    }), 200


@app.route('/questions/all', methods=['DELETE'])
def delete_all():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401

    Question.delete_all()
    return '', 204




@app.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    
    token = auth_header.split(' ')[1]
    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401
    
    question = Question.get_by_id(question_id)
    
    if question is None:
        return jsonify({'error': 'Question not found'}), 404
    
    # Get the position of the question to be deleted
    position_to_delete = question.position
    
    question.delete()
    
    # Decrement the positions of questions with positions greater than the deleted question
    for q in Question.get_all():
        if q.position > position_to_delete:
            q.position -= 1
            q.update()
    
    return jsonify({'message': 'Question deleted successfully'}), 204










@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401

    token = auth_header.split(' ')[1]
    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401

    question = Question.get_by_id(question_id)
    if question is None:
        return jsonify({'error': 'Question not found'}), 404

    data = request.get_json()

    new_position = data['position']

    if new_position != question.position:
        # If the new position is different from the current position
        old_position = question.position

        if new_position > old_position:
            # If the new position is greater than the old position, increment the positions of questions in between
            for q in Question.get_all():
                if q.id != question.id and old_position < q.position <= new_position:
                    q.position -= 1
                    q.update()
        else:
            # If the new position is smaller than the old position, decrement the positions of questions in between
            for q in Question.get_all():
                if q.id != question.id and new_position <= q.position < old_position:
                    q.position += 1
                    q.update()

        question.position = new_position
        question.update()

    question.title = data['title']
    question.text = data['text']
    question.image = data['image']
    question.possibleAnswers = json.dumps(data['possibleAnswers'])
    question.update()

    if 'possibleAnswers' in data:
        Answer.delete_by_question_id(question_id)
        for answer_data in data['possibleAnswers']:
            answer = Answer(
                question_id=question.id,
                text=answer_data['text'],
                is_correct=answer_data['isCorrect']
            )
            answer.save()

    return jsonify({'message': 'Question updated successfully'}), 204










@app.route('/participations', methods=['POST'])
def create_participation():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401

    data = request.get_json()
    participation = Participation(
        user_id=user_id,
        question_id=data['questionId'],
        answer_id=data['answerId']
    )
    participation.save()

    return jsonify({'id': participation.id}), 200


@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401

    Participation.delete_all()
    return '', 204


@app.route('/participations/<int:participation_id>', methods=['DELETE'])
def delete_participation(participation_id):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401

    participation = Participation.get_by_id(participation_id)
    if participation is None:
        return jsonify({'error': 'Participation not found'}), 404

    participation.delete()
    return jsonify({'message': 'Participation deleted successfully'}), 204





@app.route('/scores', methods=['GET'])
def get_scores():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401
    token = auth_header.split(' ')[1]

    try:
        user_id = decode_token(token)
    except JwtError as e:
        return jsonify({'error': str(e)}), 401

    scores = Score.get_by_user_id(user_id)
    scores_data = []
    for score in scores:
        scores_data.append({
            'id': score.id,
            'participation_id': score.participation_id,
            'score': score.score
        })

    return jsonify({'scores': scores_data}), 200

if __name__ == "__main__":
    app.run()

