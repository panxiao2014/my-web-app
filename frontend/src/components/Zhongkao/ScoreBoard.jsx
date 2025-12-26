import { useState, useEffect } from 'react'
import ScoreInput from './ScoreInput'
import Dropdown from './Dropdown'
import { ZHONGKAO_CONFIG } from '../../config/appConfig'

function ScoreBoard({ scores, updateScores, updateValidation }) {
  const scoreConfigs = ZHONGKAO_CONFIG.pages.scorepage.scores
  const [validationState, setValidationState] = useState({})

  // Initialize validation state for all courses
  useEffect(() => {
    const initialState = {}
    scoreConfigs.forEach((_, index) => {
      initialState[index] = false
    })
    setValidationState(initialState)
  }, [])

  // Check if all courses are valid
  useEffect(() => {
    const allValid = Object.values(validationState).every(isValid => isValid === true)
    updateValidation(allValid)
  }, [validationState, updateValidation])

  // Calculate total score
  const calculateTotal = () => {
    return scoreConfigs.reduce((total, config, index) => {
      const score = Number(scores[index]) || 0
      return total + score
    }, 0)
  }

  const handleScoreChange = (index, value) => {
    updateScores(index, value)
  }

  const handleValidationChange = (index, isValid) => {
    setValidationState(prev => ({
      ...prev,
      [index]: isValid
    }))
  }

  return (
    <div className="zhongkao-scoreboard" data-testid="scoreboard">
      <h2>{ZHONGKAO_CONFIG.pages.scorepage.title}</h2>
      
      <div className="zhongkao-scores-grid">
        {scoreConfigs.map((config, index) => {
          const isRange = config.range.length === 2
          
          if (isRange) {
            // Range input: user enters a number between min and max
            return (
              <ScoreInput
                key={index}
                title={config.title}
                value={scores[index] || ''}
                minScore={config.range[0]}
                maxScore={config.range[1]}
                onChange={(value) => handleScoreChange(index, value)}
                onValidationChange={(isValid) => handleValidationChange(index, isValid)}
              />
            )
          } else {
            // Dropdown: user selects from specific values
            return (
              <Dropdown
                key={index}
                title={config.title}
                value={scores[index] || ''}
                options={config.range.map(String)}
                onChange={(value) => {
                  handleScoreChange(index, value)
                  handleValidationChange(index, value !== '')
                }}
              />
            )
          }
        })}
      </div>

      <div className="zhongkao-total-score" data-testid="total-score">
        <strong>{ZHONGKAO_CONFIG.pages.scorepage.totalScore}</strong>
        <span className="zhongkao-total-value">{calculateTotal()}</span>
      </div>
    </div>
  )
}

export default ScoreBoard