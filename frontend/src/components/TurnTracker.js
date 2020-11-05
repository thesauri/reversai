import React from 'react'

const TurnTracker = ({ player }) => {
  const currentPlayerStyle = {
    margin: '20px',
    textAlign: 'center',
  }
  return (
    <div style={currentPlayerStyle}>
      current turn: {player}
    </div>
  )
}

export default TurnTracker
