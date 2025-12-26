import { useState, useEffect } from 'react'
import { COMMON_CONFIG } from '../../config/appConfig'

function ScoreInput({ title, value, minScore, maxScore, onChange, onValidationChange }) {
  const [error, setError] = useState('')
  const validationMessages = COMMON_CONFIG.validation.score

  const validateScore = (scoreValue) => {
    // Empty value is invalid
    if (scoreValue === '') {
      setError('')
      return false
    }

    const score = Number(scoreValue)

    // Check if within range
    if (score < minScore || score > maxScore) {
      const errorMessage = validationMessages.outOfRange
        .replace('{min}', minScore)
        .replace('{max}', maxScore)
      setError(errorMessage)
      return false
    }

    setError('')
    return true
  }

  const handleChange = (e) => {
    const inputValue = e.target.value
    const isValid = validateScore(inputValue)
    onChange(inputValue)
    if (onValidationChange) {
      onValidationChange(isValid)
    }
  }

  // Prevent non-numeric characters from being typed
  const handleKeyDown = (e) => {
    // Allow control keys
    if (
      e.key === 'Backspace' ||
      // Allow Ctrl/Cmd shortcuts
      (e.ctrlKey || e.metaKey)
    ) {
      return
    }
  
    // Prevent non-numeric characters
    if (!/^[0-9]$/.test(e.key)) {
      e.preventDefault()
    }
  }

  // Validate on mount
  useEffect(() => {
    const isValid = validateScore(value)
    if (onValidationChange) {
      onValidationChange(isValid)
    }
  }, [])

  return (
    <div className="zhongkao-score-input">
      <label className="zhongkao-input-label" data-testid="score-input-label">{title}</label>
      <input
        type="number"
        data-testid="score-input-field"
        className={`zhongkao-input-field ${error ? 'error' : ''}`}
        value={value}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        min={minScore}
        max={maxScore}
      />
      {error && <div className="zhongkao-error-message" data-testid="score-input-error">{error}</div>}
    </div>
  )
}

export default ScoreInput