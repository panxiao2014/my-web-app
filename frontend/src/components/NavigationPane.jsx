function NavigationPane({ activeApp, setActiveApp }) {
    return (
      <nav className="navigation-pane">
        <button
          className={`nav-button ${activeApp === 'App1' ? 'active' : ''}`}
          onClick={() => setActiveApp('App1')}
        >
          App1
        </button>
        <button
          className={`nav-button ${activeApp === 'App2' ? 'active' : ''}`}
          onClick={() => setActiveApp('App2')}
        >
          App2
        </button>
      </nav>
    )
  }
  
  export default NavigationPane