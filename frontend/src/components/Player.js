import React from 'react'

const Player = ({ player, col }) => {
  const style = {
    textAlign: 'center',
    gridColumnStart: col,
  }
  const headerStyle = {
    fontSize: '1rem',
    fontWeight: '900',
    letterSpacing: '0.1em',
  }

  return (
    <div style={style}>
      <h2 style={headerStyle}>{player.playerColor.toUpperCase()}</h2>
      <div>{player.name}</div>
      <div>Made by {player.creator}</div>
    </div>
  )
}

export default Player
