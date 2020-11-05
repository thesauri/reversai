import React from 'react'
import TurnTracker from './TurnTracker'
import Player from './Player'

const PlayerInfo = ({ currentPlayer }) => {
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
      <div>
        <TurnTracker player={currentPlayer}/>
      </div>
      <div style={infoBoxStyle}>
        <Player player={player1} col={1}/>
        <Player player={player2} col={2}/>
      </div>
    </div>
  )
}

export default PlayerInfo
