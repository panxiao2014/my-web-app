import { ZHONGKAO_CONFIG } from '../../config/appConfig'

function Summary({ userInfo }) {
  const summaryConfig = ZHONGKAO_CONFIG.pages.summarypage
  const scoreConfigs = ZHONGKAO_CONFIG.pages.scorepage.scores
  const totalScoreLabel = ZHONGKAO_CONFIG.pages.scorepage.totalScore

  // Calculate total score
  const calculateTotal = () => {
    return userInfo.scores.reduce((total, score) => {
      return total + (Number(score) || 0)
    }, 0)
  }

  return (
    <div className="zhongkao-summary" data-testid="summary">
      <h2>{summaryConfig.title}</h2>

      <div className="zhongkao-summary-section">
        <div className="zhongkao-summary-item">
          <span className="zhongkao-summary-label">{summaryConfig.nameLabel}</span>
          <span className="zhongkao-summary-value" data-testid="summary-name">{userInfo.name}</span>
        </div>

        <div className="zhongkao-summary-item">
          <span className="zhongkao-summary-label">{summaryConfig.genderLabel}</span>
          <span className="zhongkao-summary-value" data-testid="summary-gender">{userInfo.gender}</span>
        </div>
      </div>

      <div className="zhongkao-summary-section">
        <h3>{summaryConfig.scoresLabel}</h3>
        <div className="zhongkao-summary-scores">
          {scoreConfigs.map((config, index) => (
            <div key={index} className="zhongkao-summary-score-item">
              <span className="zhongkao-summary-label">{config.title}</span>
              <span className="zhongkao-summary-value" data-testid={`summary-score-${index}`}>
                {userInfo.scores[index]}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="zhongkao-summary-total">
        <span className="zhongkao-summary-label">{totalScoreLabel}</span>
        <span className="zhongkao-summary-total-value" data-testid="summary-total">
          {calculateTotal()}
        </span>
      </div>
    </div>
  )
}

export default Summary