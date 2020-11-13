import React from 'react'

const Player = ({ player, col, currentPlayer, winner }) => {
  let containerStyle = {
    textAlign: 'center',
    gridColumnStart: col,
    backgroundColor: '#f0f0f0',
    color: '#999',
    padding: '20px 5px 20px 5px',
    border: '1px solid #ddd',
    width: '100%'
  }
  if (player.playerColor === currentPlayer) {
    containerStyle = {
      ...containerStyle,
      border: '1px solid black',
      color: 'black',
      backgroundColor: 'white',
    }
  }
  if (player.playerColor === winner) {
    containerStyle.backgroundColor = '#79c3bb'
    containerStyle.color = 'black'
  }

  const headerStyle = {
    fontSize: '1rem',
    fontWeight: '900',
    letterSpacing: '0.1em',
  }

  return (
    <div style={containerStyle}>
      <h2 style={headerStyle}>{player.playerColor.toUpperCase()}</h2>
      <div>{player.name}</div>
      <div>Made by {player.author}</div>
    </div>
  )
}

export default Player
