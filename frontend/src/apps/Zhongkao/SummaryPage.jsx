import { useEffect } from 'react'
import Summary from '../../components/Zhongkao/Summary'

function SummaryPage({ userInfo, updateValidation }) {
  // Summary page is always valid (just displaying info)
  useEffect(() => {
    updateValidation(true)
  }, [updateValidation])

  return (
    <div className="zhongkao-page">
      <Summary userInfo={userInfo} />
    </div>
  )
}

export default SummaryPage