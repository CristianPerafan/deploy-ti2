from flask import Flask
from dotenv import load_dotenv
from src.expert_system.expertSystem import Event, ExpertPsychologicalAnalysis, Symptoms, Patient
from src.expert_system.recommendations import generic_recommendations
from src.models.models import db
from src.views.views import *
import os

app = Flask(__name__)



app.secret_key = os.getenv('SECRET')




# Database configuration
# env

load_dotenv()

user = 'expert'
password = 'Azkn9BnPzpQ4BiALkA4oIITUTJUJJAoY'
host = 'dpg-cpd9jrnsc6pc738oeubg-a'
port = '5432'
database ='expert_system'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




# db initialization
db.init_app(app)

engine = ExpertPsychologicalAnalysis()



@app.route('/')
def landing_page():
    return landing_page_view()
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_view()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return register_view()

@app.route('/home', methods=['GET', 'POST'])
def home():
    return home_view()


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    engine.reset()
    return render_template('chat.html')


@app.route('/chat/recommendations',methods=['GET', 'POST'])
def chat_results():
    greetin_msg  = engine.greeting
    symptoms = list(set(engine.results))

    activities = []

    resources = []

    for symptom in symptoms:
        symptom_attributes =   next((item for item in generic_recommendations if item["id"] == symptom), None)

        if symptom_attributes:
            activities += [activity for activity in symptom_attributes['activities']]
            resources += [resource for resource in symptom_attributes['resources']]



    return render_template(
        'chat_results.html', 
         greeting=greetin_msg,
         activities=activities,
         resources=resources)


@app.route('/initialize',methods=['GET', 'POST'])
def initialize_engine():
    engine.reset()
    engine.msg_buffer = []
    return 'Engine initialized!'




@app.route('/symptoms',methods=['GET', 'POST'])
def symptoms():

    if request.method == 'POST':
        data = request.get_json()
        intrusion = data['intrusionSymptoms']
        negative = data['negativeMoodSymptoms']
        dissociative = data['dissociationSymptoms']
        avoidance = data['avoidanceSymptoms']
        engine.declare(Symptoms(intrusion_symptoms=intrusion, negative_mood=negative, dissociative_symptoms=dissociative, avoidance_symptoms=avoidance, arousal_symptoms=0))
        #engine.run()

        return 'OK', 200
    

@app.route('/traumatic-events',methods=['GET', 'POST'])
def traumatic_event():
    if request.method == 'POST':
        data = request.get_json()
        selectedEvents = data['selectedEvents']
        for event_name in selectedEvents:
            engine.declare(Event(name=event_name))

        engine.run()
        return 'OK', 200
    


@app.route('/psychoactive_substances',methods=['POST'])
def consume_psychoactive_substances():
    if request.method == 'POST':
        data = request.get_json()
        consume = data['selectedValue']
        if consume == 'True':
            engine.declare(Patient(consumes_psychoactive_substances=True))
        elif consume == 'False':
            engine.declare(Patient(consumes_psychoactive_substances=False))
        return 'OK', 200


@app.route('/agressive_impulses',methods=['POST'])
def agressive_impulses():
    if request.method == 'POST':
        data = request.get_json()
        consume = data['selectedValue']
        if consume == 'True':
            engine.declare(Patient(agressive_impulses=True))
        elif consume == 'False':
            engine.declare(Patient(agressive_impulses=False))
        return 'OK', 200


@app.route('/depresion_anxiety_state',methods=['POST'])
def depresion_state():
    if request.method == 'POST':
        data = request.get_json()
        consume = data['selectedValue']
        consumeanx = data['selectedValueAnx']
        if consume == 'True':
            engine.declare(Patient(Depression=True))
        elif consume == 'False':
            engine.declare(Patient(Depression=False))
        
        if consumeanx == 'True':
            engine.declare(Patient(Anxiety=True))
        elif consumeanx == 'False':
            engine.declare(Patient(Anxiety=False))


        return 'OK', 200



if __name__ == '__main__':
    app.run(debug=True)