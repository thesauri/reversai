import React from 'react'
import Tile from './Tile'

const Reversi = ({ board, handleClick }) => {
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
          />
        ))
      })}
    </div>
  )
}

export default Reversi
