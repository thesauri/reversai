import React from 'react'
import Tile from './Tile'

const Reversi = ({ board, handleClick }) => {
  const style = {
    display: 'inline-grid',
    gridGap: '2px',
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
          />
        ))
      })}
    </div>
  )
}

export default Reversi
