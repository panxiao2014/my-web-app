function Dropdown({ title, value, options, onChange }) {
    const handleChange = (e) => {
      onChange(e.target.value)
    }
  
    return (
      <div className="zhongkao-dropdown">
        <label className="zhongkao-input-label">{title}</label>
        <select
          className="zhongkao-select-field"
          data-testid="dropdown-select"
          value={value}
          onChange={handleChange}
        >
          <option value="">-- 请选择 --</option>
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