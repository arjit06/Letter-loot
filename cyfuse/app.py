from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teams.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    
with app.app_context():
    db.create_all()


# Example word and its hint
word_hint = {
    'word': 'example',
    'hint': 'This is an example hint.'
}

var="lakshadeep"

# Hints for English letters

letter_hints={
    'A': 'go to the library',
    'B': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'C': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'D': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence',
    'E': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'F': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'G': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'H': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'I': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'J': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'K': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'L': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'M': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'N': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'O': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'P': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'Q': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'R': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'S': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'T': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'U': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'V': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'W': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'X': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'Y': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence', 
    'Z': 'Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quo, dolorum? Expedita animi vel, repudiandae perferendis consequence'
}



# Temporary storage for team names (for demo purposes)
team_info={"name":""}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        team_pass=request.form.get('team_pass')
        
        existing_team = Team.query.filter_by(name=team_name,password=team_pass).first()
        if not existing_team:
            return render_template('login.html', error='Incorrect credentials')
        
        team_info['name']=team_name

        # new_team = Team(name=team_name)
        # db.session.add(new_team)
        # db.session.commit()
        
        # teams.append(team_name)  # Store team name (you might use a database in a real app)
        return redirect(url_for('game'))
        # return render_template('game.html',team_info=team_info)
    return render_template('login.html')





@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        team_pass=request.form.get('team_pass')
        
        existing_team = Team.query.filter_by(name=team_name).first()
        if existing_team:
            return render_template('signup.html', error='Team name already exists.')

        new_team = Team(name=team_name, password=team_pass)
        db.session.add(new_team)
        db.session.commit()
        
        # print(team_name)
        # teams.append(team_name)  # Store team name (you might use a database in a real app)
        return redirect(url_for('game'))
    return render_template('signup.html')



@app.route('/game')
def game():
    print(var)
    return render_template('game.html',letter_hints=letter_hints)

def get_data():
    flask_variable = "Data from Flask via AJAX!"
    return jsonify({'data': flask_variable})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
