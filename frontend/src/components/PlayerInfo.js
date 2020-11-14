import React from 'react'
import Player from './Player'

const PlayerInfo = ({ currentPlayer, winner, players, score }) => {
  const infoBoxStyle = {
    display: 'grid',
    width: '586px',
    margin: '0px 10px 10px 0px',
  }
  
  return (
    <div>
      <div style={infoBoxStyle}>
        <Player player={{...players.black, playerColor: 'black'}} col={1} currentPlayer={currentPlayer} winner={winner} score={score.black} />
        <Player player={{...players.white, playerColor: 'white'}} col={2} currentPlayer={currentPlayer} winner={winner} score={score.white} />
      </div>
    </div>
  )
}

export default PlayerInfo
