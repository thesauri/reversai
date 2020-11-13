import React from 'react'
import Player from './Player'

const PlayerInfo = ({ currentPlayer, winner, players }) => {
  const infoBoxStyle = {
    display: 'grid'
  }
  
  return (
    <div>
      <div style={infoBoxStyle}>
        <Player player={{...players.black, playerColor: 'black'}} col={1} currentPlayer={currentPlayer} winner={winner}/>
        <Player player={{...players.white, playerColor: 'white'}} col={2} currentPlayer={currentPlayer} winner={winner}/>
      </div>
    </div>
  )
}

export default PlayerInfo
