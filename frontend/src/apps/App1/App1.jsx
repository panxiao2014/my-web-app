import { useState } from 'react'
import Button from '../../components/App1/Button'
import { sendPing } from './api'
import '../../styles/App1.css'

function App1() {
  const [response, setResponse] = useState('')
  const [loading, setLoading] = useState(false)

  const handleButtonClick = async () => {
    setLoading(true)
    try {
      const result = await sendPing()
      setResponse(result)
    } catch (error) {
      setResponse('Error: Could not connect to backend')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app1-container">
      <h1>App1</h1>
      <Button 
        onClick={handleButtonClick} 
        label={loading ? 'Loading...' : 'Click Me'}
      />
      {response && (
        <div className="app1-response">
          {response}
        </div>
      )}
    </div>
  )
}

export default App1