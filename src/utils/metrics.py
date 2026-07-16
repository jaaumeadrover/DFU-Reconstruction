import numpy as np
import csv
"""
TITLE: metrics.py
DATE: 02/03/2024
AUTHOR: Jaume Adrover Fernández
DESCRIPTION: script containing registration quality metrics (fitness, RMSE,
correspondence set size) collection and CSV export.
"""

def getAvgValue(list,value):
    sum=0
    if value == 'fitness':
        for item in list:
            sum=sum+item.fitness
    elif value =='rmse':
        for item in list:
            sum = sum + item.inlier_rmse
    else:
        for item in list:
            sum=sum+np.asarray(item.correspondence_set).size
    return sum/len(list)



class Metrics3D:

    def __init__(self,size):
        self.size = size
        self._fitness = [None] * size
        self._rmse = [None] * size
        self._corrsp_set = [None] * size

    @property
    def fitness(self):
        return self._fitness

    @property
    def rmse(self):
        return self._rmse

    @property
    def corrsp_set(self):
        return self._corrsp_set

    def setScore(self, score, i):
        self._fitness[i] = score.fitness
        self._rmse[i] = score.inlier_rmse
        self._corrsp_set[i] = np.asarray(score.correspondence_set).size

    def write_to_csv(self, file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['fitness', 'rmse', 'correspondence_set_size'])  # Header row

            for i in range(self.size):
                if self.fitness[i] is not None and self.rmse[i] is not None and self.corrsp_set[i] is not None:
                    writer.writerow([self.fitness[i], self.rmse[i], self.corrsp_set[i]])