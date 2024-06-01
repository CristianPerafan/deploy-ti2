from experta import *
from src.bayesian_network.BayesianNetwork import inference

class Symptoms(Fact):
    pass


class Traumatic_Events(Fact):
    pass

class Separation_Events(Fact):
    pass

class Event(Fact):
    pass


class Patient(Fact):
    pass


class ExpertPsychologicalAnalysis(KnowledgeEngine):

    msg_buffer = []

    results = []


    greeting = "Hola soy Vilbot,Gracias por completar las preguntas. Hemos analizado tus respuestas y tenemos algunas observaciones y recomendaciones para ti. Es importante recordar que los resultados proporcionados no son un diagnóstico médico, pero pueden servir como una guía para entender mejor tu bienestar emocional y mental."

    @DefFacts()
    def _initial_fact(self):
        yield Traumatic_Events(traumatic_events=["Accidente de Transito", "Catastrofe Natural", "Violencia de genero",
                                              "Accidente de trabajo", "Violencia familiar"])
        yield Separation_Events(separation_events=["Separation Discomfort", "Loss Concern", 
                                               "Adverse Event Anxiety", "Fear of Leaving", 
                                               "Fear of Solitude", "Fear of Sleeping", 
                                               "Separation Nightmares", "Physical Symptoms"])



    @Rule(Symptoms(intrusion_symptoms=MATCH.i,
                   negative_mood=MATCH.n,
                   dissociative_symptoms=MATCH.d, 
                   avoidance_symptoms=MATCH.a, 
                   arousal_symptoms=MATCH.ar),
          TEST(lambda i, n, d, a, ar : i + n + d + a + ar >= 5), Fact(direct_relation_with_traumatic_event=True))
    def manifestation_of_post_traumatic_symptoms(self, i, n, d, a, ar):
        message = "POST_TRAUMATIC_STRESS_SYMPTOMS"
        self.results.append(message)
        print(message)
        self.declare(Fact(manifestation_of_ptc_symptom=True))




    @Rule(Patient(consumes_psychoactive_substances=False),
          Traumatic_Events(traumatic_events=MATCH.traumatic_events),
          AS.event << Event(name=MATCH.event_name),
          Event(name="Accidente de Transito"))
    def traumatic_event_response(self):
        self.declare(Fact(TraumaticEvent=True))
        result = inference.map_query(variables=['AcuteStressDisorder'], evidence={'TraumaticEvent': 1})
        if result['AcuteStressDisorder'] == 1:
            message = "HIGH_PROBABILITY_OF_ACUTE_STRESS_DISORDER"
            self.results.append(message)
            print(message)
            self.declare(Fact(AcuteStressDisorder=True))
    
    @Rule(Symptoms(intrusion_symptoms=0, arousal_symptoms=0),
        Separation_Events(separation_events=MATCH.separation_events),
        Event(name="Fear of Sleeping"))
    def insomnia_inference(self):
        self.declare(Fact(SleepIssues=True))
        result = inference.map_query(variables=['InsomniaDisorder'], evidence={'SleepIssues': 1})
        if result['InsomniaDisorder'] == 1:
            message = "HIGH_PROBABILITY_OF_INSOMNIA_DISORDER"
            self.results.append(message)
            print(message)
            self.declare(Fact(InsomniaDisorder=True))


    @Rule(Traumatic_Events(traumatic_events=MATCH.traumatic_events),
          AS.event << Event(name=MATCH.event_name),
          TEST(lambda traumatic_events, event_name: event_name in traumatic_events))
    def direct_relation_with_traumatic_event(self):
        message = "DIRECT_RELATION_WITH_TRAUMATIC_EVENT"
        self.results.append(message)
        self.declare(Fact(direct_relation_with_traumatic_event=True))
        print(message)

        


    @Rule(Separation_Events(separation_events=MATCH.separation_events),
        AS.event << Event(name=MATCH.event_name),
        TEST(lambda separation_events, event_name: event_name in separation_events))
    def separation_discomfort(self):
        message = "EXPERIENCING_SEPARATION_DISCOMFORT"
        print(message)
        self.results.append(message)
        self.declare(Fact(separation_discomfort=True))
        
    

    @Rule(Fact(manifestation_of_ptc_symptom=True),
        Fact(direct_relation_with_traumatic_event=True),
        NOT(Patient(consumes_psychoactive_substances=True)))
    def acute_stress_disorder(self):
        message = "EXPERIENCING_ACUTE_STRESS_DISORDER"
        self.results.append(message)
        print(message)
        self.declare(Fact(acute_stress_disorder=True))


    @Rule(Patient(consumes_psychoactive_substances=False),
        Separation_Events(separation_events=MATCH.separation_events),
        Event(name="Separation Discomfort"))
    def separation_anxiety_response(self):
        self.declare(Fact(SeparationAnxietyEvent=True))
        result = inference.map_query(variables=['SeparationAnxietyDisorder'], evidence={'SeparationEvent': 1})
        if result['SeparationAnxietyDisorder'] == 1:
            message = "HIGH_PROBABILITY_OF_SEPARATION_ANXIETY_DISORDER"
            self.results.append(message)
            print(message)
            self.declare(Fact(SeparationAnxietyDisorder=True))


    @Rule(Fact(separation_discomfort=True),
        Patient(consumes_psychoactive_substances=False))
    def separation_anxiety_disorder(self):
        message = "EXPERIENCING_SEPARATION_ANXIETY_DISORDER"
        self.results.append(message)
        print(message)
        self.declare(Fact(separation_anxiety_disorder=True))

    
    @Rule(Fact(separation_discomfort=True),
        Patient(consumes_psychoactive_substances=True))
    def separation_anxiety_disorder_substance(self):
        message = "SEPARATION_ANXIETY_WITH_SUBSTANCE_ABUSE"
        self.results.append(message)
        print(message)
        self.declare(Fact(separation_anxiety_disorder=True))

    
    @Rule(Patient(consumes_psychoactive_substances=False),
        Patient(agressive_impulses=True))
    def intermittent_explosive_disorder_response(self):
        self.declare(Fact(AggressiveImpulses=True))
        result = inference.map_query(variables=['IntermittentExplosiveDisorder'], evidence={'AggressiveImpulses': 1})
        if result['IntermittentExplosiveDisorder'] == 1:
            message = "PROBABILITY_OF_INTERMITTENT_EXPLOSIVE_DISORDER"
            self.results.append(message)
            print(message)
            self.declare(Fact(IntermittentExplosiveDisorder=True))

    
    @Rule(Patient(consumes_psychoactive_substances=True),
        Patient(agressive_impulses=True))
    def intermittent_explosive_disorder_response_substance(self):
        self.declare(Fact(AggressiveImpulses=True))
        result = inference.map_query(variables=['IntermittentExplosiveDisorder'], evidence={'AggressiveImpulses': 1})
        if result['IntermittentExplosiveDisorder'] == 1:
            message = "INTERMITTENT_EXPLOSIVE_DISORDER_WITH_SUBSTANCE_ABUSE"
            self.results.append(message)
            print(message)
            self.declare(Fact(IntermittentExplosiveDisorder=True))
    

    @Rule(Patient(consumes_psychoactive_substances=False),
        Patient(Depression=True),
        Patient(Anxiety=False))
    def medium_depression_response(self):
        self.declare(Fact(Depression=True))
        result = inference.map_query(variables=['Depression'], evidence={'Anxiety': 1})
        if result['Depression'] == 1:
            message = "MEDIUM_PROBABILITY_OF_DEPRESSION"
            self.results.append(message)
            print(message)
            self.declare(Fact(Depression=True))


    @Rule(Patient(consumes_psychoactive_substances=True),
        Patient(Depression=True),
        Patient(Anxiety=False))
    def substance_use_disorder_response(self):
        self.declare(Fact(SubstanceUseDisorder=True))
        message = "HIGH_PROBABILITY_OF_SUBSTANCE_USE_DISORDER"
        self.results.append(message)
        print(message)
        self.declare(Fact(SubstanceUseDisorder=True))

    
    @Rule(Patient(consumes_psychoactive_substances=False),
        Patient(Depression=True),
        Patient(Anxiety=True))
    def high_depression_response(self):
        self.declare(Fact(Depression=True))
        result = inference.map_query(variables=['Depression'], evidence={'Anxiety': 1})
        if result['Depression'] == 1:
            message = "HIGH_PROBABILITY_OF_DEPRESSION"
            self.results.append(message)
            print(message)
            self.declare(Fact(Depression=True))

    @Rule(Patient(consumes_psychoactive_substances=False),
          Event(name="Distrust"),
          Patient(Anxiety=True))
    def distrust_response(self):
        self.declare(Fact(Distrust=True))
        message = "PARANOID_PERSONALITY_DISORDER"
        self.results.append(message)
        print(message)
        self.declare(Fact(Paranoid_Personality_Disorder=True))

    
    @Rule(Patient(consumes_psychoactive_substances=False),
      Event(name="Distrust"),
      Patient(Depression=True))
    def paranoid_personality_with_anxiety_response(self):
        self.declare(Fact(Distrust=True))
        message = "PARANOID_PERSONALITY_DISORDER_WITH_DEPRESSION"
        self.results.append(message)
        print(message)
        self.declare(Fact(Paranoid_Personality_Disorder=True))


    
    @Rule(Patient(consumes_psychoactive_substances=False),
          Event(name="Fear"),
          Patient(Anxiety=True))
    def panic_response(self):
        self.declare(Fact(Fear=True))
        message = "PANIC_DISORDER"
        self.results.append(message)
        print(message)
        self.declare(Fact(Panic_Disorder=True))

    
    @Rule(Patient(consumes_psychoactive_substances=False),
          Event(name="NotEat"),
          Patient(Depression=True))
    def not_eat_response(self):
        self.declare(Fact(NotEat=True))
        message = "RESTRICTIVE_FOOD_INTAKE_DISORDER"
        self.results.append(message)
        print(message)
        self.declare(Fact(Restrictive_Food_Intake_Disorder=True))



if __name__ == '__main__':
    engine = ExpertPsychologicalAnalysis()
    engine.reset()
    engine.msg_buffer = []
    engine.run()
    