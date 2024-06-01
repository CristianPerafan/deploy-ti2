from experta import *
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

model = BayesianNetwork([('TraumaticEvent', 'AcuteStressDisorder'),
                         ('SeparationEvent', 'SeparationAnxietyDisorder'),
                         ('Stress', 'Anxiety'),
                         ('Anxiety', 'Depression'),
                         ('SleepIssues', 'InsomniaDisorder'),
                         ('AggressiveImpulses', 'IntermittentExplosiveDisorder')])


cpd_traumatic_event = TabularCPD(variable='TraumaticEvent', variable_card=2, values=[[0.8], [0.2]])

cpd_acute_stress = TabularCPD(
    variable='AcuteStressDisorder', 
    variable_card=2,
    values=[[0.7, 0.4], [0.3, 0.6]], 
    evidence=['TraumaticEvent'], 
    evidence_card=[2])

cpd_separation_event = TabularCPD(
    variable='SeparationEvent', 
    variable_card=2, 
    values=[[0.6], [0.4]])

cpd_separation_anxiety = TabularCPD(
    variable='SeparationAnxietyDisorder', 
    variable_card=2,
    values=[[0.5, 0.2], [0.5, 0.8]], 
    evidence=['SeparationEvent'], 
    evidence_card=[2])

cpd_stress = TabularCPD(
    variable='Stress', 
    variable_card=2, 
    values=[[0.7], [0.3]])

cpd_anxiety = TabularCPD(
    variable='Anxiety', 
    variable_card=2,
    values=[[0.8, 0.5], [0.2, 0.5]], 
    evidence=['Stress'], 
    evidence_card=[2])

cpd_depression = TabularCPD(
    variable='Depression', 
    variable_card=2,
    values=[[0.9, 0.4], [0.1, 0.6]], 
    evidence=['Anxiety'], 
    evidence_card=[2])

cpd_sleep_issues = TabularCPD(
    variable='SleepIssues', 
    variable_card=2, 
    values=[[0.7], [0.3]])

cpd_insomnia = TabularCPD(
    variable='InsomniaDisorder', 
    variable_card=2,
    values=[[0.6, 0.2], [0.4, 0.8]], 
    evidence=['SleepIssues'], 
    evidence_card=[2])

cpd_aggressive_impulses = TabularCPD(
    variable='AggressiveImpulses', 
    variable_card=2, 
    values=[[0.6], [0.4]])

cpd_intermit_explosive = TabularCPD(
    variable='IntermittentExplosiveDisorder', 
    variable_card=2,
    values=[[0.7, 0.3], [0.3, 0.7]], 
    evidence=['AggressiveImpulses'], 
    evidence_card=[2])

model.add_cpds(cpd_traumatic_event, cpd_acute_stress, cpd_separation_event, cpd_separation_anxiety,
               cpd_stress, cpd_anxiety, cpd_depression, cpd_sleep_issues, cpd_insomnia,
               cpd_aggressive_impulses, cpd_intermit_explosive)


assert model.check_model()
inference = VariableElimination(model)

class Event(Fact):
    pass

class RelatedEvents(Fact):
    pass

class Symptoms(Fact):
    pass

class Patient(Fact):
    pass

class Expert(KnowledgeEngine):
    @DefFacts()
    def initial_facts(self):
        yield RelatedEvents(traumatic_events=["Car accident", "Earth quake"])
        yield RelatedEvents(separation_events=["Separation Discomfort", "Loss Concern", 
                                               "Adverse Event Anxiety", "Fear of Leaving", 
                                               "Fear of Solitude", "Fear of Sleeping", 
                                               "Separation Nightmares", "Physical Symptoms"])
        yield Symptoms(intrusion_symptoms=0, negative_mood=0, dissociative_symptoms=0, 
                       avoidance_symptoms=0, arousal_symptoms=0)
        yield Patient(consumes_psychoactive_substances=False)
        yield Fact(acute_stress_disorder=False)
        yield Fact(separation_anxiety_disorder=False)
        yield Fact(depression_disorder=False)
        yield Fact(insomnia_disorder=False)
        yield Fact(intermittent_explosive_disorder=False)
        yield Fact(schizoid_personality_disorder=False)
        yield Fact(avoidant_restrictive_food_intake_disorder=False)
        yield Fact(panic_disorder=False)
        yield Fact(post_traumatic_stress_disorder=False)
        yield Fact(paranoid_personality_disorder=False)

        """
        Presence of nine or more of the following symptoms in any of the five categories after the traumatic event: 
        Intrusion symptoms, Negative mood,Dissociative symptoms,Avoidance symptoms and Arousal symptoms.
        """


    @Rule(Symptoms(intrusion_symptoms=MATCH.i,
                   negative_mood=MATCH.n,
                   dissociative_symptoms=MATCH.d, 
                   avoidance_symptoms=MATCH.a, 
                   arousal_symptoms=MATCH.ar),
          TEST(lambda i, n, d, a, ar : i + n + d + a + ar >= 9))
    def manifestation_of_post_traumatic_symptoms(self, i, n, d, a, ar):
        print("The patient is experiencing post traumatic stress symptoms")
        self.declare(Fact(manifestation_of_ptc_symptom=True))


    @Rule(RelatedEvents(traumatic_events=MATCH.traumatic_events),
          AS.event << Event(name=MATCH.event_name),
          TEST(lambda traumatic_events, event_name: event_name in traumatic_events))
    def direct_relation_with_traumatic_event(self):
        print("The patient has direct relation with the traumatic event")
        self.declare(Fact(direct_relation_with_traumatic_event=True))


    @Rule(RelatedEvents(separation_events=MATCH.separation_events),
          AS.event << Event(name=MATCH.event_name),
          TEST(lambda separation_events, event_name: event_name in separation_events))
    def separation_discomfort(self):
        print("The patient is experiencing separation discomfort")
        self.declare(Fact(separation_discomfort=True))


    @Rule(Fact(manifestation_of_ptc_symptom=True),
          Fact(direct_relation_with_traumatic_event=True),
          NOT(Patient(consumes_psychoactive_substances=True)))
    def acute_stress_disorder(self):
        print("*** The patient is experiencing acute stress disorder ***")
        self.declare(Fact(acute_stress_disorder=True))


    @Rule(Fact(separation_discomfort=True),
          Patient(consumes_psychoactive_substances=False))
    def separation_anxiety_disorder(self):
        print("*** The patient is experiencing separation anxiety disorder ***")
        self.declare(Fact(separation_anxiety_disorder=True))


    @Rule(Fact(rule_test=True))
    def bayesian_inference(self):
        query_result = inference.query(variables=['Depression'], evidence={'Stress': 1})
        print(f"Probability of Depression given Stress: {query_result}")
        self.declare(Fact(probability_of_depression=query_result))


    @Rule(Fact(probability_of_depression=MATCH.prob))
    def assess_depression_risk(self, prob):
        if prob['Depression'][1] > 0.5:  # Si la probabilidad de depresión es mayor al 50%
            print("The patient is at high risk of depression.")
            self.declare(Fact(high_risk_of_depression=True))


    @Rule(Fact(high_risk_of_depression=True),
          Patient(consumes_psychoactive_substances=False))
    def depression_intervention(self):
        print("*** The patient should consider immediate psychological intervention ***")


    @Rule(Patient(consumes_psychoactive_substances=False),
          RelatedEvents(traumatic_events=MATCH.traumatic_events),
          TEST(lambda traumatic_events: "Car accident" in traumatic_events))
    def traumatic_event_response(self):
        self.declare(Fact(TraumaticEvent=True))
        result = inference.map_query(variables=['AcuteStressDisorder'], evidence={'TraumaticEvent': 1})
        if result['AcuteStressDisorder'] == 1:
            print("High probability of Acute Stress Disorder")
            self.declare(Fact(AcuteStressDisorder=True))

    @Rule(Symptoms(intrusion_symptoms=0, arousal_symptoms=0),
          RelatedEvents(separation_events=MATCH.separation_events),
          TEST(lambda separation_events: "Fear of Sleeping" in separation_events))
    def insomnia_inference(self):
        self.declare(Fact(SleepIssues=True))
        result = inference.map_query(variables=['InsomniaDisorder'], evidence={'SleepIssues': 1})
        if result['InsomniaDisorder'] == 1:
            print("High probability of Insomnia Disorder")
            self.declare(Fact(InsomniaDisorder=True))

    

if __name__ == "__main__":

    print("Welcome to the Psychological Expert System CLI")
    print("Please select an option from the menu below:")
    
    while True:
        print("\nMenu:")
        print("1. Enter Symptoms")
        print("2. Enter Event")
        print("3. Run Expert System")
        print("4. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            intrusion = int(input("Enter Intrusion Symptoms (0-5): "))
            negative = int(input("Enter Negative Mood (0-5): "))
            dissociative = int(input("Enter Dissociative Symptoms (0-5): "))
            avoidance = int(input("Enter Avoidance Symptoms (0-5): "))
            arousal = int(input("Enter Arousal Symptoms (0-5): "))
            symptoms = Symptoms(intrusion_symptoms=intrusion, negative_mood=negative, dissociative_symptoms=dissociative, avoidance_symptoms=avoidance, arousal_symptoms=arousal)
        
        elif choice == '2':
            event_name = input("Enter Event (e.g., Car accident): ")
            event = Event(name=event_name)

        elif choice == '3':
            expert = Expert()
            expert.reset()
            if 'symptoms' in locals():
                expert.declare(symptoms)
            if 'event' in locals():
                expert.declare(event)
            expert.run()

        elif choice == '4':
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")