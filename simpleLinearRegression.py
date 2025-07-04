import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

class SimpleLinearRegression:
    def __init__(self, file_path): # get numpy array
        self.loc = ''
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] # to support Traditional Chinese
        plt.rcParams['axes.unicode_minus'] = False # to deal with '-'0.149
        # self.monthX:
        # to store years from strat to end
        # 3d structure: nparr(nparr(npint32)), ex: [[1993], ..., [2023]]
        self.monthX = []
        # self.monthY:
        # to store every month's sea level from start year to end year
        # 4d structure: list(nparr(nparr(npfloat64))), ex: [[[0.035], ..., [0.149]], ..., [[-0.017], ..., [0.046]]]
        self.monthY = []
        for month in range(12):
            self.monthY.append([])
        with open(file_path, 'r') as f:
            self.stationName = os.path.basename(file_path)[:-11] # '_dealed.txt' => -11
            next(f)
            count = 0
            for line in f:
                row = line.strip().split('\t') # every row is a list, row[0]: time, row[1]: level
                month = int(row[0][-2:])
                # add years from start to end to self.monthX
                if month == 1:
                    self.monthX.append([int(row[0][:4])])
                # classify by month
                self.monthY[month-1].append([float(row[1])])
        # transform to numpy array
        for i in range(12):
            self.monthX = np.array(self.monthX)
            self.monthY[i] = np.array(self.monthY[i])
    
    def train_test(self):
        # January ~ December's data and models
        self.models = [] # to store models of Janaury ~ December
        self.train_scores = [] # a list to store train_score of January ~ December
        self.test_scores = [] # a list to store test_score of January ~ December
        self.coefs = []
        self.intercepts = []
        self.train_mse = []
        self.test_mse = []
        self.x_future = []
        self.y_future = []

        for i in range(12):
            # train
            x_train, x_test, y_train, y_test = train_test_split(self.monthX, self.monthY[i], test_size = 0.2, random_state = 42)
            model = LinearRegression()
            model.fit(x_train, y_train) # train
            train_score = model.score(x_train, y_train)
            test_score = model.score(x_test, y_test)

            ## add the single object to the set
            self.models.append(model)
            self.train_scores.append(train_score)
            self.test_scores.append(test_score)
            self.coefs.append(model.coef_[0][0])
            self.intercepts.append(model.intercept_[0])

            # test
            y_pred_train = model.predict(x_train)
            y_pred_test = model.predict(x_test)
            train_mse = mean_squared_error(y_train, y_pred_train)
            test_mse = mean_squared_error(y_test, y_pred_test)
            self.train_mse.append(train_mse)
            self.test_mse.append(test_mse)

            # predict
            start_predict_year = int(self.monthX[len(self.monthX)-1][0]) + 1
            end_predict_year = start_predict_year + 50
            future_years = np.arange(start_predict_year, end_predict_year + 1)
            self.x_future = future_years.reshape(-1, 1)
            self.y_future.append(model.predict(self.x_future))

            # level of January ~ December variate by year
            plt.clf()
            startYear = int(self.monthX[0][0])            
            endYear = int(self.x_future[len(self.x_future) - 1][0])
            x = np.linspace(startYear, endYear, 100)
            y = x * model.coef_[0][0] + model.intercept_[0]
            plt.plot(x, y, c = '#73BF00', label = 'y = coef * x + intercept')
            plt.scatter(self.monthX, self.monthY[i], color = '#C07AB8', label = 'original data')
            plt.scatter(self.x_future, self.y_future[i], color = '#AE8F00', label = 'predict data')
            plt.legend()
            plt.xlabel('time')
            plt.ylabel('level')
            plt.title(self.transNumToStr(i) + ' in ' + self.stationName + ' from ' + str(startYear) + ' to ' + str(endYear))
            
            # save graph
            imageFolderPath = "./Graphs_month"
            if not os.path.exists(imageFolderPath):
                os.makedirs(imageFolderPath)
            file_path = os.path.join(imageFolderPath, self.stationName + "_" + self.transNumToStr(i) + ".png")
            plt.savefig(file_path)

    def writeTrainTestResults(self):
        imageFolderPath = "./train_testResults"
        if not os.path.exists(imageFolderPath):
            os.makedirs(imageFolderPath)
        file_path = os.path.join(imageFolderPath, self.stationName + ".txt")

        with open(file_path, 'w') as result:
            if self.stationName == '成功' or self.stationName == '高雄' or self.stationName == '將軍' or self.stationName == '蟳廣嘴' or self.stationName == '蘭嶼':
                self.loc = 'south' # 成功, 高雄, 將軍, 蟳廣嘴, 蘭嶼 -> south
            elif self.stationName == '竹圍' or self.stationName == '基隆' or self.stationName == '蘇澳':
                self.loc = 'north' # 竹圍, 基隆, 蘇澳 -> north
            else:
                self.loc = 'middle' # 塭港 -> middle
            
            result.write('Station name: ' + self.stationName + '\n')
            result.write('Location: ' + self.loc + '\n')
            result.write('---------------------------------\n')
            for month in range(12):
                result.write('Month: ' + self.transNumToStr(month) + '\n')
                result.write('Train score: ' + str(self.train_scores[month]) + '\n')
                result.write('Test score: ' + str(self.test_scores[month]) + '\n')
                result.write('Train MSE: ' + str(self.train_mse[month]) + '\n')
                result.write('Test MSE: ' + str(self.test_mse[month]) + '\n')
                result.write('Coefficient: ' + str(self.coefs[month]) + '\n')
                result.write('Intercept: ' + str(self.intercepts[month]) + '\n')
                result.write('-----------------\n')
    
    def transNumToStr(self, i):
        month = ['January', 'Faburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        return month[i]
    
    def drawAll(self):
        # deal with lists: predicted's whole period lists
        x_whole = np.concatenate((self.monthX, self.x_future))
        y_whole = []
        for i in range(12):
            y_whole.append(np.concatenate((self.monthY[i], self.y_future[i])))
        
        # save original + predicted data
        imageFolderPath = "./DataAll"
        if not os.path.exists(imageFolderPath):
            os.makedirs(imageFolderPath)
        file_path = os.path.join(imageFolderPath, self.stationName + "_all.txt")
        with open(file_path, 'w') as f:
            f.write('time\tlevel\n')
            for i in range(len(x_whole)):
                f.write(str(x_whole[i][0]) + '\n')
                for j in range(12):
                    f.write('\t' + str(j+1) + '\t' + str(y_whole[j][i][0]) + '\n')
        
        # draw all
        x = []
        for year in x_whole:
            for i in range(12):
                if i < 10:
                    x.append(str(year[0]) + '0' + str(i+1))
                else:
                    x.append(str(year[0]) + str(i+1))

        ## re-labeling x
        tempX = np.array(x)
        ### calculate x range
        x_start = int(tempX[0][:4])
        x_end = int(tempX[len(x)-1][:4])
        x_range = x_end - x_start
        ### space of years
        space = round(x_range / 12.2)
        x_ticks = np.arange(x_start, x_end + 1, space)
        ### middle of x-axis
        x_middle = x_start + x_range // 2
        ### calculate every scale's position in x-axis
        x_tick_indices = np.linspace(0, len(x) - 1, len(x_ticks), dtype = int)
        ### new label of x-axis
        x_tick_labels = [str(year) for year in x_ticks]

        y = [] # numpy array
        tempY = [] # list
        year = 0 # init
        totalyears = len(y_whole[0])
        for year in range(totalyears):
            for month in range(len(y_whole)): # len(y_whole) == 12
                y.append(y_whole[month][year])
                tempY.append(str(y_whole[month][year][0]))

        plt.clf()
        plt.plot(x, y, label = 'year-level-plot')
        plt.xlabel('Time (year)')
        plt.xticks(x_tick_indices, x_tick_labels, rotation = 'horizontal')
        plt.ylabel('Level (m)')
        plt.title(self.stationName + 'station\'s sea leve variation from ' + str(x_start) + ' to ' + str(x_end) )

        # save graph
        imageFolderPath = "./Graphs_all"
        if not os.path.exists(imageFolderPath):
            os.makedirs(imageFolderPath)
        file_path = os.path.join(imageFolderPath, self.stationName + ".png")
        plt.savefig(file_path)

        return tempY
    
    def main_control(self):
        self.train_test()
        self.writeTrainTestResults()
        return self.loc, self.drawAll()