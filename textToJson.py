from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import re

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/')
def home():
    return render_template("index.html")

def parse_event(text):
    event = {}
    text = text.lower().strip()

    goal_pattern = r"(own goal by (\w+))|(goal by (\w+)( penalty)?( assisted by (\w+))?)"
    goal_match = re.match(goal_pattern, text)

    if goal_match:
        if goal_match.group(1):  
            event['type'] = 'goal'
            event['scorer'] = goal_match.group(2).capitalize()
            event['goal_type'] = 'Own'
        else:  
            event['type'] = 'goal'
            event['scorer'] = goal_match.group(4).capitalize()  
            goal_type = 'Normal' if not goal_match.group(5) else 'Penalty'

            if goal_match.group(7):  
                event['goal_type'] = 'Assisted'
                event['assist'] = goal_match.group(7).capitalize()  
            else:
                event['goal_type'] = goal_type

        return event

    sub_pattern = r"(\w+) (substituted|sub) (\w+)"
    sub_match = re.match(sub_pattern, text)

    if sub_match:
        event['type'] = 'substitution'
        event['player_in'] = sub_match.group(1).capitalize()
        event['player_out'] = sub_match.group(3).capitalize()
        return event

    foul_pattern = r"foul (red|yellow|none)? card? by (\w+)"
    foul_match = re.match(foul_pattern, text)

    if foul_match:
        event['type'] = 'foul'
        event['foul_by'] = foul_match.group(2).capitalize()

        card_type = foul_match.group(1) if foul_match.group(1) else 'none'
        event['card'] = f'{card_type.capitalize()} card' if card_type != 'none' else 'none'

        return event

    defended_pattern = r"defended by (\w+)"
    defended_match = re.match(defended_pattern, text)

    if defended_match:
        event['type'] = 'defended'
        event['defender'] = defended_match.group(1).capitalize()
        return event

    saved_pattern = r"saved by (\w+)"
    saved_match = re.match(saved_pattern, text)

    if saved_match:
        event['type'] = 'saved'
        event['saved_by'] = saved_match.group(1).capitalize()
        return event

    return {"error": "Event format not recognized"}

@app.route('/parse-event', methods=['GET', 'POST'])
def parse_event_api():
    if request.method == 'GET':
        return jsonify({"message": "Use POST to send data to this endpoint"}), 405

    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid input, 'text' key is required"}), 400

    text = data['text']
    result = parse_event(text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
