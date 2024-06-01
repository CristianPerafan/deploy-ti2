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




