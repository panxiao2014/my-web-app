import { useState, useEffect } from 'react'

function TextInput({ title, value, onChange, onValidationChange }) {
  const [error, setError] = useState('')

  const validateInput = (inputValue) => {
    // Check if input begins with empty spaces
    if (inputValue.length > 0 && inputValue[0] === ' ') {
      setError('Name should not begin with empty spaces')
      return false
    }
    // Check if input is not empty
    if (inputValue.trim() === '') {
      setError('')
      return false
    }
    setError('')
    return true
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
        className={`zhongkao-input-field ${error ? 'error' : ''}`}
        value={value}
        onChange={handleChange}
      />
      {error && <div className="zhongkao-error-message">{error}</div>}
    </div>
  )
}

export default TextInput