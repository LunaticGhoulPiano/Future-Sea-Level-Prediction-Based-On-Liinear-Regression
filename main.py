# Data source: https://opendata.cwb.gov.tw/dataset/forecast/C-B0048-001
# Visualized wbesite: https://flood.firetree.net/

"""
PPT:
0. Topic
1. Abstract
2. Literature/Introduction
3. Method/Data set/Variables
4. Results/Formula
5. Discussion
6. Reference/cited
"""

import os
from anova import ANOVA
from filtering import Filtering
from dealWithMissing import DealWithMissing
from simpleLinearRegression import SimpleLinearRegression

if __name__ == '__main__':
    # filter raw data
    file_path = os.path.abspath('C-B0048-001.json')
    filtered_files_path = Filtering(file_path).filter() # list

    # fill in missing data
    dealed_files_path = []
    for single_filtered_path in filtered_files_path:
        dealed_files_path.append(DealWithMissing(single_filtered_path).main_control())
    
    # training
    loc = []
    dataSet = []
    for single_dealed_path in dealed_files_path:
        tempLoc, tempSet = SimpleLinearRegression(single_dealed_path).main_control()
        loc.append(tempLoc)
        dataSet.append(tempSet)
    
    # ANOVA
    ANOVA(loc, dataSet).main_control()