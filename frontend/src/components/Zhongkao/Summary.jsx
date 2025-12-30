import { ZHONGKAO_CONFIG } from '../../config/appConfig'
import InfoBox from './InfoBox'

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
        <InfoBox 
          title={summaryConfig.nameLabel} 
          value={userInfo.name} 
          data-testid="summary-name"
        />
        <InfoBox 
          title={summaryConfig.genderLabel} 
          value={userInfo.gender}
          data-testid="summary-gender"
        />
      </div>

      <div className="zhongkao-summary-section">
        <h3>{summaryConfig.scoresLabel}</h3>
        <div className="zhongkao-summary-scores">
          {scoreConfigs.map((config, index) => (
            <div key={index} data-testid={`summary-score-${index}`}>
              <InfoBox
                title={config.title}
                value={userInfo.scores[index]}
              />
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