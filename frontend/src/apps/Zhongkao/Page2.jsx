import { useEffect } from 'react'
import Dropdown from '../../components/Zhongkao/Dropdown'
import { ZHONGKAO_CONFIG } from '../../config/appConfig'

function Page2({ userInfo, updateUserInfo, updateValidation }) {
  const genderOptions = [ZHONGKAO_CONFIG.pages.page2.options[0], ZHONGKAO_CONFIG.pages.page2.options[1]]

  // Validate on mount and when gender changes
  useEffect(() => {
    const isValid = userInfo.gender !== ''
    updateValidation(isValid)
  }, [userInfo.gender, updateValidation])

  return (
    <div className="zhongkao-page">
      <Dropdown
        title={ZHONGKAO_CONFIG.pages.page2.title}
        value={userInfo.gender}
        options={genderOptions}
        onChange={(value) => updateUserInfo('gender', value)}
      />
    </div>
  )
}

export default Page2