import React from 'react'

const Tile = ({ tile }) => {
  const style = {
    width: '20px',
    height: '20px'
  }
  if (tile === 'white') {
    style.background = 'white'
  } else if (tile === 'black') {
    style.background = 'black'
  } else {
    style.background = 'gray' 
  }
  return (
    <button style={style}></button>
  )
}

const Row = ({ row }) => {
  return (
    <div>
      {row.map((tile, index) => (
        <Tile key={index} tile={tile} />
      ))}
    </div>
  )
}

const Othello = (props) => {
  return (
    <div>
      {props.board.map((row, index) => (
        <Row key={index} row={row} />
      ))}
    </div>
  )
}

export default Othello
