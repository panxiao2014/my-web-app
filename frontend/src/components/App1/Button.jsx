function Button({ onClick, label }) {
  return (
    <button className="app1-button" onClick={onClick}>
      {label}
    </button>
  )
}

export default Button