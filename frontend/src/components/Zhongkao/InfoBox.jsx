function InfoBox({ title, value }) {
  return (
    <div className="zhongkao-infobox">
      <span className="zhongkao-infobox-label">{title}</span>
      <span className="zhongkao-infobox-value">{value}</span>
    </div>
  )
}

export default InfoBox