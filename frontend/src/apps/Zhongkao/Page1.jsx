import TextInput from '../../components/Zhongkao/TextInput'

function Page1({ userInfo, updateUserInfo, updateValidation }) {
  return (
    <div className="zhongkao-page">
      <TextInput
        title="Your name:"
        value={userInfo.name}
        onChange={(value) => updateUserInfo('name', value)}
        onValidationChange={updateValidation}
      />
    </div>
  )
}

export default Page1