function Dropdown({ title, value, options, onChange }) {
    const handleChange = (e) => {
      onChange(e.target.value)
    }
  
    return (
      <div className="zhongkao-dropdown">
        <label className="zhongkao-input-label">{title}</label>
        <select
          className="zhongkao-select-field"
          value={value}
          onChange={handleChange}
        >
          <option value="">-- Select --</option>
          {options.map((option, index) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </select>
      </div>
    )
  }
  
  export default Dropdown