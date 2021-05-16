import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np


class FuzzyController:

    def __init__(self, n):
        low = 1 / (2 * n)
        med = 1 / n
        high = 3 / (2 * n)

        '''Generarea functiilor membre pentru logica fuzzy'''
        t1 = ctrl.Antecedent(np.arange(0, 1.0001, 0.001), 't1')
        t2 = ctrl.Antecedent(np.arange(0, 1.0001, 0.001), 't2')
        t3 = ctrl.Antecedent(np.arange(0, 1.0001, 0.001), 't3')
        self.CA = ctrl.Consequent(np.arange(0, 1.0001, 0.001), 'CA')
        pc = ctrl.Consequent(np.arange(0, 1.0001, 0.001), 'pc')
        self.MA = ctrl.Consequent(np.arange(0, 1.0001, 0.001), 'MA')
        pm = ctrl.Consequent(np.arange(0, 1.0001, 0.001), 'pm')

        t1['low'] = fuzz.trapmf(t1.universe, [0, 0, 0.25, 0.5])
        t1['medium'] = fuzz.trimf(t1.universe, [0.25, 0.5, 0.75])
        t1['high'] = fuzz.trapmf(t1.universe, [0.5, 0.75, 1.0, 1.0])

        t2['low'] = fuzz.trapmf(t2.universe, [0, 0, 0.25, 0.5])
        t2['high'] = fuzz.trapmf(t2.universe, [0.5, 0.75, 1.0, 1.0])

        t3['low'] = fuzz.trapmf(t3.universe, [0, 0, 0.25, 0.5])
        t3['medium'] = fuzz.trimf(t3.universe, [0.25, 0.5, 0.75])
        t3['high'] = fuzz.trapmf(t3.universe, [0.5, 0.75, 1.0, 1.0])

        self.CA['low'] = fuzz.trapmf(self.CA.universe, [0, 0, 0.25, 0.5])
        self.CA['medium'] = fuzz.trimf(self.CA.universe, [0.25, 0.5, 0.75])
        self.CA['high'] = fuzz.trapmf(self.CA.universe, [0.5, 0.75, 1.0, 1.0])

        pc['low'] = fuzz.trapmf(pc.universe, [0, 0, 0.25, 0.5])
        pc['medium'] = fuzz.trimf(pc.universe, [0.25, 0.5, 0.75])
        pc['high'] = fuzz.trapmf(pc.universe, [0.5, 0.75, 1.0, 1.0])

        self.MA['low'] = fuzz.trapmf(self.MA.universe, [0, 0, 0.25, 0.5])
        self.MA['medium'] = fuzz.trimf(self.MA.universe, [0.25, 0.5, 0.75])
        self.MA['high'] = fuzz.trapmf(self.MA.universe, [0.5, 0.75, 1.0, 1.0])

        pm['low'] = fuzz.trapmf(pm.universe, [0, 0, low, med])
        pm['medium'] = fuzz.trimf(pm.universe, [low, med, high])
        pm['high'] = fuzz.trapmf(pm.universe, [med, high, 1.0, 1.0])

        rule1 = ctrl.Rule(t1['low'] & t2['low'] & t3['low'],
                          [self.CA['high'], pc['high'], self.MA['high'], pm['high']])
        rule2 = ctrl.Rule(t1['low'] & t2['low'] & t3['medium'],
                          [self.CA['high'], pc['high'], self.MA['high'], pm['high']])
        rule3 = ctrl.Rule(t1['low'] & t2['low'] & t3['high'],
                          [self.CA['medium'], pc['medium'], self.MA['medium'], pm['high']])
        rule4 = ctrl.Rule(t1['low'] & t2['high'] & t3['low'],
                          [self.CA['high'], pc['medium'], self.MA['high'], pm['high']])
        rule5 = ctrl.Rule(t1['low'] & t2['high'] & t3['medium'],
                          [self.CA['medium'], pc['medium'], self.MA['medium'], pm['medium']])
        rule6 = ctrl.Rule(t1['low'] & t2['high'] & t3['high'],
                          [self.CA['medium'], pc['low'], self.MA['medium'], pm['low']])
        rule7 = ctrl.Rule(t1['medium'] & t2['low'] & t3['low'],
                          [self.CA['high'], pc['high'], self.MA['high'], pm['high']])
        rule8 = ctrl.Rule(t1['medium'] & t2['low'] & t3['medium'],
                          [self.CA['medium'], pc['medium'], self.MA['medium'], pm['medium']])
        rule9 = ctrl.Rule(t1['medium'] & t2['low'] & t3['high'],
                          [self.CA['medium'], pc['medium'], self.MA['medium'], pm['low']])
        rule10 = ctrl.Rule(t1['medium'] & t2['high'] & t3['low'],
                           [self.CA['medium'], pc['medium'],
                            self.MA['medium'], pm['medium']])
        rule11 = ctrl.Rule(t1['medium'] & t2['high'] & t3['medium'],
                           [self.CA['medium'], pc['medium'], self.MA['medium'], pm['low']])
        rule12 = ctrl.Rule(t1['medium'] & t2['high'] & t3['high'],
                           [self.CA['medium'], pc['low'], self.MA['medium'], pm['low']])
        rule13 = ctrl.Rule(t1['high'] & t2['low'] & t3['low'],
                           [self.CA['high'], pc['high'], self.MA['high'], pm['high']])
        rule14 = ctrl.Rule(t1['high'] & t2['low'] & t3['medium'],
                           [self.CA['medium'], pc['medium'], self.MA['medium'], pm['medium']])
        rule15 = ctrl.Rule(t1['high'] & t2['low'] & t3['high'],
                           [self.CA['low'], pc['medium'], self.MA['low'], pm['low']])
        rule16 = ctrl.Rule(t1['high'] & t2['high'] & t3['low'],
                           [self.CA['low'], pc['medium'], self.MA['medium'], pm['low']])
        rule17 = ctrl.Rule(t1['high'] & t2['high'] & t3['medium'],
                           [self.CA['low'], pc['low'], self.MA['low'], pm['low']])
        rule18 = ctrl.Rule(t1['high'] & t2['high'] & t3['high'],
                           [self.CA['low'], pc['low'], self.MA['low'], pm['low']])

        self.evolution_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6,
                                                  rule7, rule8, rule9, rule10, rule11,
                                                  rule12, rule13, rule14, rule15, rule16,
                                                  rule17, rule18])

        self.evolution = ctrl.ControlSystemSimulation(self.evolution_ctrl)

    def apply_rules(self, t1: float, t2: float, t3: float):
        self.evolution.input['t1'] = t1
        self.evolution.input['t2'] = t2
        self.evolution.input['t3'] = t3
        self.evolution.compute()

        ca_low = fuzz.interp_membership(self.CA.universe, fuzz.trapmf(self.CA.universe, [0, 0, 0.25, 0.5]),
                                        self.evolution.output['CA'])
        ca_medium = fuzz.interp_membership(self.CA.universe, fuzz.trimf(self.CA.universe, [0.25, 0.5, 0.75]),
                                           self.evolution.output['CA'])
        ca_high = fuzz.interp_membership(self.CA.universe, fuzz.trapmf(self.CA.universe, [0.5, 0.75, 1.0, 1.0]),
                                         self.evolution.output['CA'])

        ma_low = fuzz.interp_membership(self.MA.universe, fuzz.trapmf(self.MA.universe, [0, 0, 0.25, 0.5]),
                                        self.evolution.output['MA'])
        ma_medium = fuzz.interp_membership(self.MA.universe, fuzz.trimf(self.MA.universe, [0.25, 0.5, 0.75]),
                                           self.evolution.output['MA'])
        ma_high = fuzz.interp_membership(self.MA.universe, fuzz.trapmf(self.MA.universe, [0.5, 0.75, 1.0, 1.0]),
                                         self.evolution.output['MA'])

        if ca_medium < ca_low > ca_high:
            result_ca = "low"
        elif ca_low < ca_medium > ca_high:
            result_ca = "medium"
        else:
            result_ca = "high"

        if ma_medium < ma_low > ma_high:
            result_ma = "low"
        elif ma_low < ma_medium > ma_high:
            result_ma = "medium"
        else:
            result_ma = "high"

        return result_ca, self.evolution.output['pc'], result_ma, self.evolution.output['pm']
