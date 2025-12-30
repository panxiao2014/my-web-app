from fastapi import FastAPI
from apps.Zhongkao.utils.studentName import StudentName
from apps.Zhongkao.utils.studentSet import StudentSet
import apps.Zhongkao.config.config as GlobalConfig

async def init_zhongkao(app: FastAPI):
    print("Initializing zhongkao...")
    stuNameData = StudentName()
    stuNames = stuNameData.cerateStudentNames(GlobalConfig.StudentTotal)

    stuSet = StudentSet(stuNames)
    stuSet.categorizeStudent()

    app.state.stuNames = stuNames
    app.state.stuSet = stuSet
