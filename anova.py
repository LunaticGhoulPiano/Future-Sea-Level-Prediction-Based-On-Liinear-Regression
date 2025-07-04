import numpy as np
from scipy.stats import f_oneway

class ANOVA:
    def __init__(self, loc, dataSet):
        self.stations = {
            'loc': loc,
            'level': dataSet
        }

    def classify(self):
        station_data = {}
        for loc, level in zip(self.stations['loc'], self.stations['level']):
            if loc not in station_data:
                station_data[loc] = []
            station_data[loc].extend(level)
        return station_data

    def one_way_ANOVA(self, station_data):
        f_statistic, p_value = f_oneway(*station_data.values())
        print('f_statistic: ')
        print(f_statistic)
        print('p_value: ')
        print('{:.2e}'.format(p_value))
        if p_value == 0:
            print('p_value is zero!')
        elif p_value < 0.05:
            print('Alternative Hypothesis!')
        else:
            print('Null Hypothesis!')
    
    def main_control(self):
        self.one_way_ANOVA(self.classify())