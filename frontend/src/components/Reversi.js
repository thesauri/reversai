import React from 'react'
import Tile from './Tile'

const Reversi = ({ board, handleClick, currentPlayer, latestPosition }) => {
  const style = {
    display: 'inline-grid',
    gridGap: '2px',
    border: '1px solid #eee'
  }
  if (board === null) {
    return (<div style={{width: '576px', height: '576px'}}>Loading...</div>)
  }

  return (
    <div style={style}>
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
