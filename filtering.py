import json
import os

class Filtering:
    def __init__(self, file_path): # get Location
        self.folder_path = os.path.dirname(file_path)
        self.filtered = []
        with open(file_path, 'r', encoding='utf-8') as f:
            self.f_dict = json.load(f)
        self.locList = self.f_dict["cwbdata"]["Resources"]["Resource"]["Data"]["SeaSurfaceObs"]["Location"]

    def findStation(self, stationName): # get StationObsStatistics of the Station
        for loc in range(len(self.locList)):
            if self.locList[loc]["Station"]["StationName"] == stationName:
                break
        return self.locList[loc]["StationObsStatistics"]

    def outputFile(self, stationName, statistics): # wirte time and MeanTideLevel to txt
        self.stationName = stationName
        # generate new folder "filtered" to save filtered data
        newFolderPath = "./filteredData"
        if not os.path.exists(newFolderPath):
            os.makedirs(newFolderPath)
        # write file
        file_path = os.path.join(newFolderPath, stationName + "_filtered.txt")
        with open(file_path, 'w' ) as f:
            f.write('time\tlevel\n')
            count = 0
            for y in statistics["DataYear"]:
                    for i in range(12):
                        f.write(y)
                        if int(statistics["Monthly"][count]["DataMonth"]) < 10:
                            f.write('0')
                        f.write(statistics["Monthly"][count]["DataMonth"])
                        f.write('\t' + statistics["Monthly"][count]["MeanTideLevel"] + '\n')
                        count += 1
        self.filtered.append(file_path)

    def filter(self): # main control
        for loc in range(len(self.locList)):
            self.outputFile(self.locList[loc]["Station"]["StationName"], self.findStation(self.locList[loc]["Station"]["StationName"]))
        return self.filtered