from flask import render_template, request, session, redirect, url_for
from src.models.models import User, db
from werkzeug.security import check_password_hash, generate_password_hash
from src.config.site import questions

def landing_page_view():
    return render_template('landing.html')

def login_view():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user is None:
            return render_template('login.html', error='User not found')
        
        if not check_password_hash(user.password, password):
            return render_template('login.html', error='Incorrect password')
        
        session['user_id'] = user.id
        return redirect(url_for('home'))
        
    return render_template('login.html')

def register_view():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')

        # verify the user don't exist
        user = User.query.filter_by(email=email).first()

        if user:
            return render_template('register.html', error='User already exists')

        hashed_password = generate_password_hash(password)
        user = User(email=email, password=hashed_password, first_name=first_name, last_name=last_name, gender=gender)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')
    

def chat_view():


    # Check if session exists
    if 'question_index' not in session:
        print("Resetting session")
        session['question_index'] = 0
        session['answers'] = []
        session['bot_questions'] = []
        session['history'] = []

    # Check if session already and it is the last question
    elif session['question_index'] >= len(questions):
        print("Resetting session")
        session['question_index'] = 0
        session['answers'] = []
        session['bot_questions'] = []


    if request.method == 'POST':
        message = request.form.get('message')
        # Append the answer to the answers list

        session['answers'].append(message)
        session['question_index'] += 1
        if session['question_index'] >= len(questions):
            print("session",session['bot_questions'])
            return render_template('landing.html')


    # Append the question to the bot_questions list
    if session['question_index'] > 0:
        session['bot_questions'].append(questions[session['question_index']-1]['question'])


    history = list(zip(session['bot_questions'], session['answers']))
    
    return render_template(
        'chat.html', 
        question = questions[session['question_index']],
        bot_questions = session['bot_questions'],
        answers = session['answers'],
        history = history
    )


def home_view():
    if request.method == 'POST':
        pass

    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(id=user_id).first()

    return render_template('home.html', user=user)
