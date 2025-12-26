import { useState, useEffect } from 'react'
import { validName } from '../../utils/utils'

function NameInput({ title, value, onChange, onValidationChange }) {
  const [error, setError] = useState('')

  const validateInput = (inputValue) => {
    const { isValid, errorMessage } = validName(inputValue)
    setError(errorMessage)
    return isValid
  }

  const handleChange = (e) => {
    const inputValue = e.target.value
    const isValid = validateInput(inputValue)
    onChange(inputValue)
    if (onValidationChange) {
      onValidationChange(isValid)
    }
  }

  // Validate on mount
  useEffect(() => {
    const isValid = validateInput(value)
    if (onValidationChange) {
      onValidationChange(isValid)
    }
  }, [])

  return (
    <div className="zhongkao-text-input">
      <label className="zhongkao-input-label">{title}</label>
      <input
        type="text"
        data-testid="name-input-field"
        className={`zhongkao-input-field ${error ? 'error' : ''}`}
        value={value}
        onChange={handleChange}
      />
      {error && <div className="zhongkao-error-message" data-testid="name-input-error">{error}</div>}
    </div>
  )
}

export default NameInput