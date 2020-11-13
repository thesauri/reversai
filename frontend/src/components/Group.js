import React from 'react'
import BotInfo from './BotInfo'

const Group = ({ standings, number }) => {
  const style = {
    gridColumnStart: number,
    padding: '20px',
    margin: '20px',
    background: 'white',
    width: '300px',
  }

  const headerStyle = {
    textAlign: 'center'
  }

  return (
    <div style={style}>
      <h2 style={headerStyle}>{`GROUP ${number}`}</h2>
      <div>
      {standings.map((bot, i) => (
        <BotInfo 
          key={bot.name}
          name={bot.name}
          points={bot.points}
          annotation={bot.annotation}
          stripe={i%2===1}
        />
        ))}
      </div>
    </div>
  )
}

export default Group
