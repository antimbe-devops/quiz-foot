from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
	x = 'Ilyes'
	return f"Qui a la pire coupe ? .... {x}"

if __name__ == "__main__":
    app.run()