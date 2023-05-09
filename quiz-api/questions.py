import sqlite3

class Question:
    def __init__(self, id=None, position=None, title=None, text=None, image=None):
        self.id = id
        self.position = position
        self.title = title
        self.text = text
        self.image = image

    def save(self):
        conn = sqlite3.connect('quizdb.db')
        c = conn.cursor()
#       c.execute(f'INSERT INTO question (position, title, text, image) VALUES ({self.position}, "{self.title}", "{self.text}", "{self.image}")')
        c.execute('''INSERT INTO question (position, title, text, image) VALUES (?, ?, ?, ?)''',
                  (self.position, self.title, self.text, self.image))
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
            return Question(*row)

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
            return Question(*row)
