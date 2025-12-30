#中考成绩规则：
#语，数，外：满分150
#物理：满分70
#化学：满分50
#体育：满分60
#道法，历史，生物，地理:
#  80-100: 20
#  70-79:  16
#  60-69:  12
#  0-59:   8
#满分: 710

import random
import pandas as pd
import warnings
import apps.Zhongkao.config.config as GlobalConfig


class ScoreGen:
    def __init__(self, stuNumber, dfStudents):
        self.stuNumber = stuNumber

        warnings.simplefilter(action='ignore', category=UserWarning)
        self.dfScoreStats = pd.read_excel('apps/Zhongkao/data/2023/score.stats.2023.xlsx', dtype={"学校代码": str})
        warnings.resetwarnings()

        self.dfStudents = dfStudents
        return
    

    #根据一个排名区间，得到该区间总共有多少考生：
    def getMatchStudents(self, numRankMin, numRankMax):
        dfTemp = self.dfScoreStats[(self.dfScoreStats['累计'] > numRankMin) & (self.dfScoreStats['累计'] <= numRankMax)]
        return dfTemp['人数'].sum()

    

    #根据一分一段表，生成每个学生的中考总分：
    def generateScoresForAllStudents(self):
        stuIndex = 0
        for index, row in self.dfScoreStats.iterrows():
            score = row["分数"]
            stuNumber = row["人数"]
            
            startIdx = stuIndex
            endIdx = startIdx + stuNumber - 1

            self.dfStudents.loc[startIdx:endIdx, '总分'] = score
            stuIndex = endIdx + 1

            if(score == GlobalConfig.ScoreBottomGate):
                break
        
        return

    

    def genMyScoreAuto(self):
        myScore = {}
        myScore["语文"] = random.randint(115, 130)
        myScore["数学"] = random.randint(110, 125)
        myScore["英语"] = random.randint(125, 140)
        myScore["物理"] = random.randint(58, 69)
        myScore["化学"] = random.randint(39, 49)
        myScore["体育"] = random.randint(50, 60)
        myScore["道法"] = random.choice([20, 16])
        myScore["历史"] = random.choice([20, 16])
        myScore["生物"] = random.choice([20, 16])
        myScore["地理"] = random.choice([20, 16])
        myScore["总分"] = myScore["语文"] + myScore["数学"] + myScore["英语"] + myScore["物理"] + myScore["化学"] + myScore["体育"]\
                + myScore["道法"] + myScore["历史"] + myScore["生物"] + myScore["地理"]
        return myScore
    

    def genMyScoreArray(self):
        return [random.randint(115, 130),
                random.randint(110, 125),
                random.randint(125, 140),
                random.randint(58, 69),
                random.randint(39, 49),
                random.randint(50, 60),
                random.choice([20, 16]),
                random.choice([20, 16]),
                random.choice([20, 16]),
                random.choice([20, 16])
                ]