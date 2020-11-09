import React from 'react'
import BotInfo from './BotInfo'

const Group = ({ standings, number }) => {
  return (
    <div>
      <div>{`Group ${number}`}</div>
      <ul>
      {standings.map((bot) => (
        <BotInfo 
          name={bot.name}
          points={bot.points}
          annotation={bot.annotation}
        />
        ))}
      </ul>
    </div>
  )
}

export default Group
