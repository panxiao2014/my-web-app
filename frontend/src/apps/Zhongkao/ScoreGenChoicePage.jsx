import { useEffect, useState } from 'react'
import Dropdown from '../../components/Zhongkao/Dropdown'
import { ZHONGKAO_CONFIG } from '../../config/appConfig'
import { generateScores } from './api'

function ScoreGenChoicePage({ userInfo, updateUserInfo, updateValidation }) {
  const config = ZHONGKAO_CONFIG.pages.scoregenchoicepage
  const [isGenerating, setIsGenerating] = useState(false)

  // Validate when method changes
  useEffect(() => {
    const isValid = userInfo.scoreGenMethod !== ''
    updateValidation(isValid)
  }, [userInfo.scoreGenMethod, updateValidation])

  const handleMethodChange = async (value) => {
    updateUserInfo('scoreGenMethod', value)
    
    // If user selects "随机生成各科成绩" (index 1), generate scores
    if (value === config.options[1]) {
      setIsGenerating(true)
      try {
        const scores = await generateScores()
        updateUserInfo('scores', scores)
      } catch (error) {
        console.error('Failed to generate scores:', error)
        // You can add error handling UI here if needed
      } finally {
        setIsGenerating(false)
      }
    }
  }

  return (
    <div className="zhongkao-page">
      <Dropdown
        title={config.title}
        value={userInfo.scoreGenMethod || ''}
        options={config.options}
        onChange={handleMethodChange}
      />
      {isGenerating && (
        <div className="zhongkao-generating-message">
          正在生成成绩...
        </div>
      )}
    </div>
  )
}

export default ScoreGenChoicePage