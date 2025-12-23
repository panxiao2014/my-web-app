import { useState } from 'react'
import NavigationPane from './components/NavigationPane'
import App1 from './apps/App1/App1'
import App2 from './apps/App2/App2'
import Zhongkao from './apps/Zhongkao/Zhongkao'

function App() {
  const [activeApp, setActiveApp] = useState('App1')

  const renderApp = () => {
    switch (activeApp) {
      case 'App1':
        return <App1 />
      case 'App2':
        return <App2 />
      case 'Zhongkao':
        return <Zhongkao />
      default:
        return <App1 />
    }
  }

  return (
    <div className="app-container">
      <NavigationPane activeApp={activeApp} setActiveApp={setActiveApp} />
      <div className="app-content">
        {renderApp()}
      </div>
    </div>
  )
}

export default App