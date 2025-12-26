import ScoreBoard from '../../components/Zhongkao/ScoreBoard'
import { ZHONGKAO_CONFIG } from '../../config/appConfig'

function ScorePage({ userInfo, updateUserInfo, updateValidation }) {
  const totalCourses = ZHONGKAO_CONFIG.pages.scorepage.scores.length

  const handleScoresUpdate = (index, value) => {
    const newScores = [...(userInfo.scores || Array(totalCourses).fill(''))]
    newScores[index] = value
    updateUserInfo('scores', newScores)
  }

  return (
    <div className="zhongkao-page">
      <ScoreBoard
        scores={userInfo.scores || Array(totalCourses).fill('')}
        updateScores={handleScoresUpdate}
        updateValidation={updateValidation}
      />
    </div>
  )
}

export default ScorePage