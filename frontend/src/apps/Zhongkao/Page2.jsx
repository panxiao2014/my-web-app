import { useEffect } from 'react'
import Dropdown from '../../components/Zhongkao/Dropdown'
import { ZHONGKAO_CONFIG } from '../../config/appConfig'

function Page2({ userInfo, updateUserInfo, updateValidation }) {
  const genderOptions = [ZHONGKAO_CONFIG.pages.page2.options[0], ZHONGKAO_CONFIG.pages.page2.options[1]]

  // Validate on mount
  useEffect(() => {
    const isValid = userInfo.gender !== ''
    updateValidation(isValid)
  }, [])

  const handleChange = (value) => {
    updateUserInfo('gender', value)
    // Validate immediately after updating
    updateValidation(value !== '')
  }

  return (
    <div className="zhongkao-page">
      <Dropdown
        title={ZHONGKAO_CONFIG.pages.page2.title}
        value={userInfo.gender}
        options={genderOptions}
        onChange={handleChange}
      />
    </div>
  )
}

export default Page2