import random
from apps.Zhongkao.utils.studentSet import StudentSet
from apps.Zhongkao.utils.scoreGen import ScoreGen

async def handle_genScore(stuSet: StudentSet):    
    return {"scores": stuSet.scoreGen.genMyScoreArray()}