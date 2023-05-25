import sqlite3
import json


class Question:
    def __init__(self, id=None, position=None, title=None, text=None, image=None, possibleAnswers=None):
        self.id = id
        self.position = position
        self.title = title
        self.text = text
        self.image = image
        self.possibleAnswers = possibleAnswers

    def save(self):
        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
        possible_answers_json = json.dumps(self.possibleAnswers)  
        c.execute('''INSERT INTO question (position, title, text, image, possibleAnswers) VALUES (?, ?, ?, ?, ?)''',
                  (self.position, self.title, self.text, self.image, possible_answers_json,))
        self.id = c.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM question WHERE id=?''', (id,))
        row = c.fetchone()
        conn.close()
        if row is None:
            return None
        else:
            question = Question(*row)
            question.possibleAnswers = json.loads(question.possibleAnswers)  
            return question

    @staticmethod
    def get_by_position(position):
        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM question WHERE position=?''', (position,))
        row = c.fetchone()
        conn.close()
        if row is None:
            return None
        else:
            question = Question(*row)
            question.possibleAnswers = json.loads(question.possibleAnswers) 
            return question



    def update(self, position=None, title=None, text=None, image=None, possibleAnswers=None):
        if position is not None:
            self.position = position
        if title is not None:
            self.title = title
        if text is not None:
            self.text = text
        if image is not None:
            self.image = image
        if possibleAnswers is not None:
            self.possibleAnswers = possibleAnswers

        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
        possible_answers_json = json.dumps(self.possibleAnswers)  
        c.execute('''
            UPDATE question
            SET position=?, title=?, text=?, image=?, possibleAnswers=?
            WHERE id=?
        ''', (self.position, self.title, self.text, self.image, possible_answers_json, self.id))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
        c.execute("SELECT * FROM question")
        rows = c.fetchall()
        conn.close()

        questions = []
        for row in rows:
            question = Question(*row)
            question.possibleAnswers = json.loads(question.possibleAnswers)  
            questions.append(question)

        return questions
    


    def delete(self):
        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
        c.execute('''DELETE FROM question WHERE id=?''', (self.id,))
        conn.commit()
        conn.close()


    @staticmethod
    def delete_all():
        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
        c.execute('DELETE FROM question')
        conn.commit()
        conn.close()

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "position": self.position,
            "title": self.title,
            "text": self.text,
            "image": self.image,
            "possibleAnswers": self.possibleAnswers
        })
    

    
class Answer:
    def __init__(self, id=None, question_id=None, questionPosition=None,text=None, is_correct=None):
        self.id = id
        self.question_id = question_id
        self.questionPosition=questionPosition
        self.text = text
        self.is_correct = is_correct

    def save(self):
        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
        c.execute('''INSERT INTO answer (question_id,questionPosition, text, is_correct) VALUES (?,?, ?, ?)''',
                  (self.question_id,self.questionPosition, self.text, self.is_correct))
        self.id = c.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM answer WHERE id=?''', (id,))
        row = c.fetchone()
        conn.close()
        if row is None:
            return None
        else:
            return Answer(*row)

    @staticmethod
    def get_by_question_id(question_id):
        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM answer WHERE question_id=?''', (question_id,))
        rows = c.fetchall()
        conn.close()
        return [Answer(*row) for row in rows]

    @staticmethod
    def delete_by_question_id(question_id):
        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
        c.execute('DELETE FROM answer WHERE question_id = ?', (question_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_all():
        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
        c.execute('DELETE FROM answer')
        conn.commit()
        conn.close()

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "question_id": self.question_id,
            "text": self.text,
            "is_correct": self.is_correct
        })
    
class Participation:
    def __init__(self, id=None, playerName=None,  answers=None, score=None):
        self.id = id
        self.playerName = playerName
        self.answers = answers
        self.score = score

    def getScore(username):
        conn=sqlite3.connect('quizdb.db')
        c=conn.cursor()
        c.execute('''SELECT score FROM Participation WHERE playerName = ?''', (username,) )
        usernames = c.fetchone()[0]

        return usernames





    def getGoodAnswers():
        conn=sqlite3.connect('quizdb.db')
        c=conn.cursor()
        c.execute("""SELECT questionPosition,
                        CASE 
                            WHEN MIN(id)%4 = 0 THEN 4
                            ELSE MIN(id)%4
                        END AS goodAnswerPosition
                    FROM answer
                    WHERE is_correct = 1
                    GROUP BY questionPosition;""")
        
        results= [row[1] for row in c.fetchall()]
        return results

    def calculate_quiz_score(self):
        conn=sqlite3.connect('quizdb.db')
        c=conn.cursor()
        c.execute("""SELECT questionPosition,
                        CASE 
                            WHEN MIN(id)%4 = 0 THEN 4
                            ELSE MIN(id)%4
                        END AS goodAnswerPosition
                    FROM answer
                    WHERE is_correct = 1
                    GROUP BY questionPosition;""")
        
        results= [row[1] for row in c.fetchall()]

        score=0
        for answer,result in zip(self.answers,results):
                
                if answer==result:
                    
                    score += 1
         
        self.score = score

    def save(self):
        conn = sqlite3.connect('quizdb.db')
        print(self.playerName, self.answers)
        c = conn.cursor()
        Participation.calculate_quiz_score(self)
        c.execute('''INSERT INTO participation (playerName,  answers, score) VALUES ( ?, ?, ?)''',
                  (self.playerName, json.dumps(self.answers),self.score,))
        self.id = c.lastrowid
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
        c.execute('DELETE FROM participation WHERE id=?', (self.id,))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_all():
        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
        c.execute('DELETE FROM participation')
        conn.commit()
        conn.close()

    

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "playerName": self.playerName,
            "answers": json.dumps(self.answers),
            "score":self.score
        })
