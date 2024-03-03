from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
import pandas as pd

word_riddles=pd.read_csv("word_riddles.csv")
word=list(word_riddles['word'])
riddles=list(word_riddles['riddle'])
word_dic={}
for i,w in enumerate(word):
    word_dic[w]=riddles[i]
qr_mapping = {str(i): chr(i + ord('a') - 1) for i in range(1, 27)}
letter_riddles=pd.read_csv("letter_riddles.csv")
letter=list(letter_riddles['letter'])
rid=list(letter_riddles['riddle'])

letter_hints={}
for i,w in enumerate(letter):
    letter_hints[qr_mapping[str(w)].upper()]=rid[i]

import random
class WordManager:
    def __init__(self):
        self.word_list = word
        self.used_words = []

    def get_random_word(self):
        if not self.word_list:
            # If the word_list is empty, refill it with used_words and clear used_words
            self.word_list = self.used_words.copy()
            self.used_words.clear()

        selected_word = random.choice(self.word_list)
        self.word_list.remove(selected_word)
        self.used_words.append(selected_word)

        return selected_word

# Example usage:
word_manager = WordManager()

# for round_number in range(1, 31):
#     selected_word = word_manager.get_random_word()
#     print(f"Round {round_number}: {selected_word}")

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    time_spent = db.Column(db.Float, default=0.0)
    score = db.Column(db.Integer, default=0, nullable=False)
    current_word = db.Column(db.String(255))  # The current word being guessed
    guessed_letters = db.Column(db.String(255), default='')  # The letters guessed so far
    game_in_progress = db.Column(db.Boolean, default=False)
    start_time = db.Column(db.DateTime, default=datetime.now)  # New attribute for start time


with app.app_context():
    db.create_all()




# var=word_manager.get_random_word()

# Hints for English letters



# Temporary storage for team names (for demo purposes)
team_info={}
var=''
guessed_letters=''
guessed_letter=''
congratulations_message="Don't be smart, just think SMART"
@app.route('/login', methods=['GET', 'POST'])
def login():
    global team_info
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        team_pass = request.form.get('team_pass')

        existing_team = Team.query.filter_by(name=team_name, password=team_pass).first()
        if not existing_team:
            return render_template('login.html', error='Incorrect credentials')

        team_info['name'] = team_name
        team_info['login_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Set start time and mark game as in progress
        existing_team.start_time = datetime.now()
        existing_team.game_in_progress = True
        db.session.commit()

        return redirect(url_for('game'))
    return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def signup():
    global team_info
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        team_pass = request.form.get('team_pass')

        existing_team = Team.query.filter_by(name=team_name).first()
        if existing_team:
            return render_template('signup.html', error='Team name already exists.')

        new_team = Team(name=team_name, password=team_pass)
        new_team.start_time = datetime.now()
        new_team.game_in_progress = True
        db.session.add(new_team)
        db.session.commit()

        team_info['name'] = team_name
        team_info['login_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return redirect(url_for('game'))
    return render_template('signup.html')

@app.route('/finish_game', methods=['POST'])
def finish_game():
    team_name = team_info.get('name')
    team = Team.query.filter_by(name=team_name).first()
    if team.game_in_progress:
        team.game_in_progress = False
        elapsed_time = (datetime.now() - team.start_time).total_seconds()
        team.time_spent = elapsed_time
        db.session.commit()
    return redirect(url_for('leaderboard'))

@app.route('/game')
def game():
    global guessed_letters, congratulations_message, var
    team_name = team_info.get('name')
    team = Team.query.filter_by(name=team_name).first()

    if team.game_in_progress:
        if not team.current_word or team.current_word==None:
            team.current_word = word_manager.get_random_word()
            var=team.current_word
            print(team.current_word)
  # Replace 'var' with the logic to get a new word
            guessed_letters = '_' * (len(team.current_word))
            congratulations_message="Refresh the website to see the changes"

            db.session.commit()
        if guessed_letters == (team.current_word).lower():
            team.score += 1
            team.current_word = None
            elapsed_time = (datetime.now() - team.start_time).total_seconds()
            team.time_spent = elapsed_time
            db.session.commit()

            congratulations_message = "Congratulations! You found the complete word, refresh the website to start next round"

        return render_template('game.html', letter_hints=letter_hints, current_word=guessed_letters,
                               congratulations_message=congratulations_message,word_hint=word_dic[var])
    else:
        return redirect(url_for('leaderboard'))
    
@app.route('/process_qr_code', methods=['POST'])
def process_qr_code():
    global guessed_letters
    data = request.get_json()
    guessed_letter = qr_mapping[data.get('qrData')]
    print(guessed_letter)
    team_name = team_info.get('name')
    team = Team.query.filter_by(name=team_name).first()
    team.time_spent = (datetime.now() - team.start_time).total_seconds()
    db.session.commit()

    for i, char in enumerate(team.current_word):
        if char.lower() == guessed_letter:
            guessed_letters = guessed_letters[:i] + guessed_letter + guessed_letters[i+1:]

    return 'Success', 200


@app.route('/leaderboard')
def leaderboard():
    teams = Team.query.order_by(Team.score.desc(), Team.time_spent).all()
    return render_template('leaderboard.html', teams=teams)



   
def get_data():
    flask_variable = "Data from Flask via AJAX!"
    return jsonify({'data': flask_variable})

if __name__ == '__main__':
    app.run(debug=True)