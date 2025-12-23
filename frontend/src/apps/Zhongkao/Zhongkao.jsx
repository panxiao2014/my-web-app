import { useState } from 'react'
import Page1 from './Page1'
import Page2 from './Page2'
import '../../styles/Zhongkao.css'

function Zhongkao() {
  const [currentPage, setCurrentPage] = useState(1)
  const [userInfo, setUserInfo] = useState({
    name: '',
    gender: ''
  })
  const [isCurrentPageValid, setIsCurrentPageValid] = useState(false)

  const totalPages = 2

  const handleNext = () => {
    if (currentPage < totalPages && isCurrentPageValid) {
      setCurrentPage(currentPage + 1)
    }
  }

  const handlePrevious = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1)
    }
  }

  const updateUserInfo = (field, value) => {
    setUserInfo(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const updateValidation = (isValid) => {
    setIsCurrentPageValid(isValid)
  }

  const renderPage = () => {
    switch (currentPage) {
      case 1:
        return <Page1 userInfo={userInfo} updateUserInfo={updateUserInfo} updateValidation={updateValidation} />
      case 2:
        return <Page2 userInfo={userInfo} updateUserInfo={updateUserInfo} updateValidation={updateValidation} />
      default:
        return <Page1 userInfo={userInfo} updateUserInfo={updateUserInfo} updateValidation={updateValidation} />
    }
  }

  return (
    <div className="zhongkao-container">
      <h1>User Registration</h1>
      <div className="zhongkao-page-indicator">
        Page {currentPage} of {totalPages}
      </div>
      
      <div className="zhongkao-content">
        {renderPage()}
      </div>

      <div className="zhongkao-navigation">
        <button 
          className="zhongkao-button zhongkao-button-previous"
          onClick={handlePrevious}
          disabled={currentPage === 1}
        >
          Previous
        </button>
        <button 
          className="zhongkao-button zhongkao-button-next"
          onClick={handleNext}
          disabled={currentPage === totalPages || !isCurrentPageValid}
        >
          Next
        </button>
      </div>
    </div>
  )
}

export default Zhongkao