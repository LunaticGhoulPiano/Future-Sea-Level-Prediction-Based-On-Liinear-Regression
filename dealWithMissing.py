import os
import statistics
import numpy as np
import matplotlib.pyplot as plt

class DealWithMissing:
    def __init__(self, file_path):
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] # to support Traditional Chinese
        plt.rcParams['axes.unicode_minus'] = False # to deal with '-'0.149
        self.stationName = os.path.basename(file_path)[:-13] # '_filtered.txt' => -13
        self.data = []
        with open(file_path, 'r') as f:
            next(f) # skip 'time\tlevel\n'
            for line in f:
                row = line.strip().split('\t') # every row is a list, row[0]: time, row[1]: level
                if row[1] == '-':
                    row[1] = None
                else:
                    row[1] = float(row[1])
                self.data.append(row)

    def filter_year(self): # delete the first empty period
        # step1. judge if the first year is whole None; if not then can't goto step2
        firstYearIsWholeEmpty = True
        for i in range(12):
            if self.data[i][1] != None:
                firstYearIsWholeEmpty = False
        # step2. if the first month is None then delete whole year
        if firstYearIsWholeEmpty == True:
            count = 0
            for row in self.data:
                head = self.data[0]
                if head[1] == None:
                    count += 1
                    if count == 12:
                        count = 0
                        for j in range(12):
                            self.data.pop(0)
                else:
                    break
    
    def fill_in_with_Nearest_value_imputation(self):
        for i in range(len(self.data)):
            if self.data[i][1] is None:
                if i == 0 or i == len(self.data) - 1: # skip head and tail
                    continue
                elif self.data[i-1][1] is not None and self.data[i+1][1] is not None: # use 
                    self.data[i][1] = (self.data[i-1][1] + self.data[i+1][1]) / 2
                # else the data is still None
    
    def fill_in_with_three_imputation_mode(self, imputationMode):
        year = []
        for i in range(12):
            year.append([])
        for row in self.data:
            if row[1] == None:
                continue
            month = int(row[0][-2:])
            year[month-1].append(float(row[1]))
        
        # get each month's median value and append in medianMonthData
        medianMonthData = [] # store each value of month
        for month in year:
            if imputationMode == 'mean':
                median = statistics.mean(month)
            elif imputationMode == 'median':
                median = statistics.median(month)
            elif imputationMode == 'mode':
                median = statistics.mode(month)
            medianMonthData.append(median)
        
        # replace None to the median value of each month
        for row in self.data:
            if row[1] == None:
                row[1] = medianMonthData[int(row[0][4:])-1]
    
    def writeFile(self):
        # generate new folder "dealed" to save dealed data
        newFolderPath = "./dealedData"
        if not os.path.exists(newFolderPath):
            os.makedirs(newFolderPath)
        # write file
        file_path = os.path.join(newFolderPath, self.stationName + "_dealed.txt")
        with open(file_path, 'w') as f:
            f.write('time\tlevel\n')
            for row in self.data:
                f.write(f"{row[0]}\t{row[1]}\n") # f-string requires Python 3.6
        return file_path

    def drawData(self, imputationMode):
        plt.clf()
        x = []
        y = []
        for row in self.data:
            if row[1] != None:
                x.append(row[0])
                y.append(row[1])
        x = np.array(x)
        y = np.array(y)
        plt.plot(x, y, marker = 'o')
        plt.xlabel('Time')
        plt.ylabel('Level')
        plt.title(imputationMode)
        plt.show()
    
    def main_control(self):
        # before imputation
        ##self.drawData(self.stationName + ' station\'s orignial data')
        # delete first empty period
        self.filter_year()
        # imputation
        self.fill_in_with_Nearest_value_imputation()
        self.fill_in_with_three_imputation_mode('median') # mean/median/mode
        # after imputation
        ##self.drawData('Use median to impute data of ' + self.stationName + ' station') # mean/median/mode
        return self.writeFile()