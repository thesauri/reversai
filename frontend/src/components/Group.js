import React from 'react'
import BotInfo from './BotInfo'

const Group = ({ standings, number, playingTeams }) => {
  const style = {
    gridColumnStart: number,
    padding: '0px 0px 20px 0px',
    margin: '20px 10px 20px 10px',
    background: 'white',
    width: '250px',
    boxShadow: '0px 5px 5px #aaa'
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
          isPlaying={[playingTeams.blackTeam, playingTeams.whiteTeam].includes(bot.name)}
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
