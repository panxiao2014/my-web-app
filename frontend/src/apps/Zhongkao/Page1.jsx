import NameInput from '../../components/Zhongkao/NameInput'
import { ZHONGKAO_CONFIG } from '../../config/appConfig'

function Page1({ userInfo, updateUserInfo, updateValidation }) {
  return (
    <div className="zhongkao-page">
      <NameInput
        title={ZHONGKAO_CONFIG.pages.page1.title}
        value={userInfo.name}
        onChange={(value) => updateUserInfo('name', value)}
        onValidationChange={updateValidation}
      />
    </div>
  )
}

export default Page1