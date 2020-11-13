import React from 'react'
import Tile from './Tile'

const Reversi = ({ board, handleClick, currentPlayer, latestPosition, winner }) => {
  const style = {
    display: 'inline-grid',
    gridGap: '2px',
    border: '1px solid white',
    background: 'white',
    margin: '20px 0px 0px 20px',
    padding: '10px',
    boxShadow: '0px 5px 5px #aaa'
  }
  const winnerStyle = {
    gridArea: '4 / 1 / 6 / 9',
    zIndex: 100,
    textAlign: 'center',
    verticalAlign: 'middle',
    padding: 'auto',
    fontSize: '3.7rem',
    fontWeight: '900',
    color: 'white',
    backgroundColor: '#79c3bb',
    opacity: '90%',
  }

  if (winner === '') {
    winnerStyle.display = 'none'
  }

  if (board === null) {
    return (<div style={{width: '576px', height: '576px'}}>Loading...</div>)
  }

  return (
    <div className='board' style={style}>
      <div style={winnerStyle}>GAME OVER, WINNER: {winner} </div>
      {board.map((row, rowIndex) => {
        return row.map((tile, columnIndex) => (
          <Tile 
          key={`${rowIndex}${columnIndex}`}
          tile={tile}
          rowIndex={rowIndex}
          columnIndex={columnIndex}
          handleClick={handleClick}
          currentPlayer={currentPlayer}
          highlight={rowIndex === latestPosition[0] && columnIndex === latestPosition[1]}
          />
        ))
      })}
    </div>
  )
}

export default Reversi
