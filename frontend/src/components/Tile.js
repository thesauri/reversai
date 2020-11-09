import React from 'react'
import './Tile.css'

const Tile = ({ 
  currentPlayer,
  tile,
  rowIndex,
  columnIndex,
  handleClick,
  highlight,
}) => {
  const tileStyle = {
    width: '70px',
    height: '70px',
    gridColumnStart: columnIndex + 1,
    backgroundColor: 'rgb(230, 230, 220)',
    display: 'inline-block',
    border: 'none',
    padding: '5px 5px',
    margin: 0,
    textDecoration: 'none',
    textAlign: 'center',
    transition: 'background 250ms ease-in-out, transform 150ms ease',
    WebkitAppearance: 'none',
    MozAppearance: 'none',
  }
  const circleStyle = {
    height: '60px',
    width: '60px',
    position: 'relative',
    borderRadius: '50%',
    display: 'inline-block',
  }

  if (tile === 'white') {
    circleStyle.backgroundColor = 'white'
  } else if (tile === 'black') {
    circleStyle.backgroundColor = 'black'
  } else {
    tileStyle.cursor = 'pointer'
    circleStyle.backgroundColor = currentPlayer
    circleStyle.transition = 'all 0.2s ease 0s'
  }

  if (highlight) {
    tileStyle.border = '4px solid #79c3bb'
    tileStyle.padding = '1px'
  }

  return (
    <button onClick={() => handleClick(rowIndex, columnIndex)} style={tileStyle}>
      <span className={tile ? '': 'emptyTile'} style={circleStyle}></span>
    </button>
  )
}

export default Tile
