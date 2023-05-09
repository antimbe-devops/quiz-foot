from flask.json import JSONEncoder
from questions import Question


class QuizEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Question):
            return {
                'id': obj.id,
                'position': obj.position,
                'title': obj.title,
                'text': obj.text,
                'image': obj.image
            }
        return super().default(obj)


def question_decoder(json_data):
    if 'position' in json_data and 'title' in json_data and 'text' in json_data:
        return Question(
            position=json_data['position'],
            title=json_data['title'],
            text=json_data['text'],
            image=json_data.get('image', None)
        )
    return json_data
