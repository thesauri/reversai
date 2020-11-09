import React from 'react'
import Player from './Player'

const PlayerInfo = ({ currentPlayer, winner }) => {
  const player1 = {
    name: '0th3ll0GRINDR2000',
    creator: 'sammoa',
    playerColor: 'white',
  }
  const player2 = {
    name: 'You',
    creator: 'God',
    playerColor: 'black',
  }
  const infoBoxStyle = {
    display: 'grid'
  }
  
  return (
    <div>
      <div style={infoBoxStyle}>
        <Player player={player1} col={1} currentPlayer={currentPlayer} winner={winner}/>
        <Player player={player2} col={2} currentPlayer={currentPlayer} winner={winner}/>
      </div>
    </div>
  )
}

export default PlayerInfo
