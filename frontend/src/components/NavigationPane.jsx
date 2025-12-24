function NavigationPane({ activeApp, setActiveApp }) {
    return (
      <nav className="navigation-pane">
        <button
          data-testid="nav-app1"
          className={`nav-button ${activeApp === 'App1' ? 'active' : ''}`}
          onClick={() => setActiveApp('App1')}
        >
          App1
        </button>
        
        <button
          data-testid="nav-app2"
          className={`nav-button ${activeApp === 'App2' ? 'active' : ''}`}
          onClick={() => setActiveApp('App2')}
        >
          App2
        </button>

        <button
          data-testid="nav-zhongkao"
          className={`nav-button ${activeApp === 'Zhongkao' ? 'active' : ''}`}
          onClick={() => setActiveApp('Zhongkao')}
        >
          中考
        </button>
      </nav>
    )
  }
  
  export default NavigationPane