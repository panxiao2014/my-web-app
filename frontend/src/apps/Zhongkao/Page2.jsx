import { useEffect } from 'react'
import Dropdown from '../../components/Zhongkao/Dropdown'

function Page2({ userInfo, updateUserInfo, updateValidation }) {
  const genderOptions = ['Female', 'Male']

  // Validate on mount and when gender changes
  useEffect(() => {
    const isValid = userInfo.gender !== ''
    updateValidation(isValid)
  }, [userInfo.gender, updateValidation])

  return (
    <div className="zhongkao-page">
      <Dropdown
        title="Gender:"
        value={userInfo.gender}
        options={genderOptions}
        onChange={(value) => updateUserInfo('gender', value)}
      />
    </div>
  )
}

export default Page2