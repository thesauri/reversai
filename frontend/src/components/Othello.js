import React from 'react'
import Tile from './Tile'

const Othello = (props) => {
  const style = {
    display: 'inline-grid',
    gridGap: '2px',
  }

  return (
    <div style={style}>
      {props.board.map((row, rowIndex) => {
        return row.map((tile, columnIndex) => (
          <Tile 
          key={`${rowIndex}${columnIndex}`}
          tile={tile}
          rowIndex={rowIndex}
          columnIndex={columnIndex}
          />
        ))
      })}
    </div>
  )
}

export default Othello
