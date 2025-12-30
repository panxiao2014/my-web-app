import pandas as pd
import random


import apps.Zhongkao.config.config as GlobalConfig
from apps.Zhongkao.utils.scoreGen import ScoreGen


class StudentSet:
    def __init__(self, stuNames):
        #所有报考学生的记录：
        self.dfStudents = pd.DataFrame(stuNames)

        #报考学生总数：
        self.stuNumber = self.dfStudents.shape[0]

        #参加第二批次填报志愿的学生:
        self.stuForSecondRoundNum = 0
        self.dfStuForSecondRound = pd.DataFrame()

        self.scoreGen = ScoreGen(self.stuNumber, self.dfStudents)

        self.myName = ""
        #append a tag so my name know who is myself in the dataframe:
        self.myNameTag = "(mySelf)"
        self.myTotalScore = 0
        self.myScoreRank = 0

        #init score degrade:
        self.dfScoreCounts = pd.DataFrame(columns = ['分数', '人数'])

        #重高线
        self.privilegeScoreGate = 0
        return
    

    #学生分类：统招或调剂
    def categorizeStudent(self):
        numLocalStudent = GlobalConfig.StudentTotal - GlobalConfig.EdgeStudentTotal
        numEdgeStudent = GlobalConfig.EdgeStudentTotal

        lst1 = ['统招' for _ in range(numLocalStudent)]
        lst2 = ['调剂' for _ in range(numEdgeStudent)]

        catList = lst1 + lst2
        random.shuffle(catList)
        self.dfStudents['类型'] = catList
        return
    

    def showStudents(self):
        print(self.dfStudents)
        return
    

    def getStuForSecondRoundNum(self):
        return self.stuForSecondRoundNum
    

    def appendMyself(self, mySelf):
        self.myName = mySelf["姓名"]
        mySelf["姓名"] = "{}{}".format(self.myName, self.myNameTag)
        mySelf["类型"] = "统招"
        self.myTotalScore = mySelf["总分"]

        #获取自己的得分排名：
        scoreLevel = self.myTotalScore
        if(scoreLevel > GlobalConfig.ScoreTopGate):
            scoreLevel = GlobalConfig.ScoreTopGate
        if(scoreLevel < GlobalConfig.ScoreBottomGate):
            scoreLevel = GlobalConfig.ScoreBottomGate
        self.myScoreRank = self.dfScoreCounts.loc[self.dfScoreCounts["分数"] == scoreLevel, "累计"].values[0]  

        #change each item in dict into list, so it can be added to the dataframe:
        mySelf["姓名"] = [mySelf["姓名"]]
        mySelf["性别"] = [mySelf["性别"]]
        mySelf["语文"] = [mySelf["语文"]]
        mySelf["数学"] = [mySelf["数学"]]
        mySelf["英语"] = [mySelf["英语"]]
        mySelf["物理"] = [mySelf["物理"]]
        mySelf["化学"] = [mySelf["化学"]]
        mySelf["体育"] = [mySelf["体育"]]
        mySelf["道法"] = [mySelf["道法"]]
        mySelf["历史"] = [mySelf["历史"]]
        mySelf["生物"] = [mySelf["生物"]]
        mySelf["地理"] = [mySelf["地理"]]
        mySelf["总分"] = [mySelf["总分"]]
        mySelf["排名"] = self.myScoreRank

        myDf = pd.DataFrame(mySelf)
        self.dfStudents = pd.concat([self.dfStudents, myDf], ignore_index = True)
        return
    

    def getScoreRank(self, score):
        scoreLevel = score
        if(scoreLevel > GlobalConfig.ScoreTopGate):
            scoreLevel = GlobalConfig.ScoreTopGate
        return self.dfScoreCounts.loc[self.dfScoreCounts["分数"] == scoreLevel, "累计"].values[0]
    

    def getMyScoreRank(self):
        return self.myScoreRank
    

    def getMyTotalScore(self):
        return self.myTotalScore
    

    def generateScoreCount(self):
        scoreStats = self.dfStudents["总分"].value_counts().sort_index(ascending=False)

        self.dfScoreCounts['分数'] = scoreStats.index
        self.dfScoreCounts['人数'] = scoreStats.values
        self.dfScoreCounts = self.dfScoreCounts.sort_values(by='分数', ascending=False)
        return
    

    def generateCumulativeScore(self):
        self.dfScoreCounts['累计'] = self.dfScoreCounts['人数'].cumsum()
        self.dfScoreCounts.iloc[0, self.dfScoreCounts.columns.get_loc('累计')] = self.dfScoreCounts.iloc[0, self.dfScoreCounts.columns.get_loc('人数')]
        return
     
    
    def generateScores(self):
        #generate each student's score
        self.scoreGen.generateScoresForAllStudents()

        #generate score count:
        self.generateScoreCount()

        #generate cumulative count for each score:
        self.generateCumulativeScore()

        #add cumulative rank to each student:
        mergedDf = pd.merge(self.dfStudents, self.dfScoreCounts, left_on="总分", right_on="分数", how="left")
        self.dfStudents["排名"] = mergedDf["累计"]
        return

    

    #获取重高线：在一份一段表中，累计人数达到第二批所有需要通过考试录取的名额总数时，对应的分数即为重点线
    def getPrivilegeScoreGate(self, schoolStats):
        secondRoundStuQuota = schoolStats.getSecondRoundStuQuota()
        dfScoreCountTemp = self.dfScoreCounts[self.dfScoreCounts["累计"] <= secondRoundStuQuota]
        
        self.privilegeScoreGate = int(dfScoreCountTemp["分数"].min())
        return self.privilegeScoreGate


    def trimDownStudents(self):
        dfTemp = self.dfStudents.copy()
        dfTemp = dfTemp.sort_values(by='总分', ascending=False)

        #去掉省重线以下的学生：
        dfTemp = dfTemp[dfTemp["总分"] >= self.privilegeScoreGate]

        #去掉统招生中，拿到市指标的学生:
        myName = "{}{}".format(self.myName, self.myNameTag)
        dfStuWithCityQuota = dfTemp[(dfTemp["姓名"] != myName) & (dfTemp["类型"] == "统招")].sample(n=GlobalConfig.CityQuotaTotal)
        dfTemp.drop(dfStuWithCityQuota.index, inplace=True)

        #去掉艺体生：
        dfTalentStudentQuota = dfTemp[(dfTemp["姓名"] != myName)].sample(n=GlobalConfig.TalentQuotaTotal)
        dfTemp.drop(dfTalentStudentQuota.index, inplace=True)

        self.dfStuForSecondRound = dfTemp.copy()
        self.stuForSecondRoundNum = self.dfStuForSecondRound.shape[0]

        #增加志愿填报列：
        for i in range(GlobalConfig.NumShoolToApply):
            self.dfStuForSecondRound["{}".format(GlobalConfig.OrderMap[i])] = None

        #增加选取策略列：
        self.dfStuForSecondRound["选取策略"] = None

        return
    

    #保存我填报的志愿：
    def saveMyApplying(self, dictMyApply):
        for i in range(GlobalConfig.NumShoolToApply):
            self.dfStuForSecondRound.loc[self.dfStuForSecondRound["姓名"] == (self.myName + self.myNameTag), "{}".format(GlobalConfig.OrderMap[i])] = dictMyApply["{}".format(GlobalConfig.OrderMap[i])]
        return
        