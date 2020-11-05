import React from 'react'
import Tile from './Tile'

const Reversi = ({ board, setBoard, currentPlayer, setCurrentPlayer }) => {
  const getOtherPlayer = player => {
    return player === 'black' ? 'white' : 'black'
  }

  const handleClick = (rowIndex, columnIndex) => {
    const newBoard = [...board]
    newBoard[rowIndex][columnIndex] = currentPlayer
    setBoard(newBoard)
    setCurrentPlayer(getOtherPlayer(currentPlayer))
  }

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
