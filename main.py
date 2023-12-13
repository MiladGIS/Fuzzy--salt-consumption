"""
fuzzy_expert library will be used
file is used for creating Mamdani`fuzzy inference system

"""
import matplotlib.pyplot as plt
from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference

from ipywidgets import interact, widgets

# dictionary of the variables of the problem will be defined
variables = {
    "age": FuzzyVariable(
        universe_range = (1, 99),
        terms = {
            "Teen": [(1, 1), (5, 0.8), (10, 0.6), (15, 0.3), (20, 0)],
            "Young": [(10, 0), (15, 0.5), (20, 1), (25, 1), (30, 0.7), (35, 0.5), (40, 0.2), (45, 0)],
            "Old": [(40, 0), (50, 0.3), (60, 0.6), (70, 0.9), (80, 1)],
        },
    ),
    # Diastolic Blood Pressure
    # pressure in the arteries when the heart rests between beats
    "DBP": FuzzyVariable(
        universe_range = (40, 100),
        terms = {
            "Low_DBP": [(40, 1), (50, 0.5), (60, 0)],
            "Medium_DBP": [(50, 0), (60, 0.5), (70, 1), (80, 0.5), (90, 0)],
            "High_DBP": [(80, 0), (90, 0.5), (100, 1)],
        },
    ),
    # Systolic Blood Pressure
    # pressure heart exerts on the walls of arteries each time it beats
    "SBP": FuzzyVariable(
        universe_range = (70, 190),
        terms = {
            "Low_SBP": [(70, 1), (80, 0.5), (90, 0)],
            "Medium_SBP": [(80, 0), (90, 0.5), (100, 1), (110, 1), (120, 0.5), (130, 0)],
            "High_SBP": [(130, 0), (140, 0.5), (150, 1)],
        },
    ),
    "saltConsumption": FuzzyVariable(
        # amount of salt consupmtion in milligrams
        universe_range = (1, 6),
        terms = {
            "Low": [(2, 1), (2.5, 0.5), (3, 0)],
            "Medium": [(2, 0), (2.5, 0.5), (3, 1), (3.5, 1), (4, 0.5), (4.5,0)],
            "High": [(3.5, 0), (4, 0.5), (4.5, 1)],
        },
    ),
}

plt.figure(figsize = (10, 2.5))
#variables["saltConsumption"].plot()
variables["SBP"].plot()
#variables["SBP"].plot()

rules = [
    FuzzyRule(
        premise = [
            ("age", "Old"),
            ("AND", "DBP", "High_DBP"),
            ("AND", "SBP", "High_SBP"),
        ],
        consequence = [("saltConsumption", "Low")],
    ),
    FuzzyRule(
        premise = [ 
            ("age", "Old"),
            ("AND", "DBP", "Low_DBP"),
            ("AND", "SBP", "Low_SBP"),
        ],
        consequence = [("saltConsumption", "Medium")],
    ),
    FuzzyRule(
        premise = [ 
            ("age", "Old"),
            ("AND", "DBP", "Medium_DBP"),
            ("AND", "SBP", "Medium_SBP"),
        ],
        consequence = [("saltConsumption", "Medium")],
    ),
    FuzzyRule(
        premise = [
            ("age", "Young"),
            ("AND", "DBP", "High_DBP"),
            ("AND", "SBP", "High_SBP"),
        ],
        consequence = [("saltConsumption", "Low")],
    ),
    FuzzyRule(
        premise = [
            ("age", "Young"),
            ("AND", "DBP", "Low_DBP"),
            ("AND", "SBP", "Low_SBP"),
        ],
        consequence = [("saltConsumption", "High")],
    ),
    FuzzyRule(
        premise = [
            ("age", "Young"),
            ("AND", "DBP", "Medium_DBP"),
            ("AND", "SBP", "Medium_SBP"),
        ],
        consequence = [("saltConsumption", "Medium")],
    ),
    FuzzyRule(
        premise = [
            ("age", "Teen"),
            ("AND", "DBP", "Low_DBP"),
            ("AND", "SBP", "Low_SBP"),
        ],
        consequence = [("saltConsumption", "Medium")],
    ),
    FuzzyRule(
        premise = [
            ("age", "Teen"),
            ("AND", "DBP", "High_DBP"),
            ("AND", "SBP", "High_SBP"),
        ],
        consequence = [("saltConsumption", "Low")],
    ),
    FuzzyRule(
        premise = [
            ("age", "Teen"),
            ("AND", "DBP", "Medium_DBP"),
            ("AND", "SBP", "Medium_SBP"),
        ],
        consequence = [("saltConsumption", "Low")],
    )
]

print(rules[0])
print()
print(rules[1])

model = DecompositionalInference(and_operator = "min",or_operator = "max",
                                 implication_operator = "Rc", composition_operator = "max-min",
                                 production_link = "max", defuzzification_operator = "cog")

model(variables = variables, rules = rules, age = 17, DBP = 89, SBP = 127)

#plt.figure(figsize = (10, 6))
#model.plot(variables = variables, rules = rules, age = 19, DBP = 79, SBP = 150)

# aslo an interface designed for more user control
# Better be used in jupyter IDE

def demo(age, DBP, SBP):
    plt.figure(figsize = (10,6))
    model.plot(variables = variables, rules = rules, age = age,
               DBP = DBP, SBP = SBP)
    
interact(demo, age = widgets.FloatSlider(min = 1, max = 99),
         DBP = widgets.FloatSlider(min = 40, max = 100),
         SBP = widgets.FloatSlider(min = 70, max = 190))
