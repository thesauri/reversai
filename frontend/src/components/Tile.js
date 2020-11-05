import React from 'react'

const Tile = ({ 
  tile,
  rowIndex,
  columnIndex,
  handleClick
}) => {
  const tileStyle = {
    width: '4rem',
    height: '4rem',
    gridColumnStart: columnIndex + 1,
    backgroundColor: 'rgb(230, 230, 220)',
    display: 'inline-block',
    border: 'none',
    padding: '0.2rem 0.2rem',
    margin: 0,
    textDecoration: 'none',
    textAlign: 'center',
    transition: 'background 250ms ease-in-out, transform 150ms ease',
    WebkitAppearance: 'none',
    MozAppearance: 'none',
  }
  const circleStyle = {
    height: '3.5rem',
    width: '3.5rem',
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
  }

  return (
    <button onClick={() => handleClick(rowIndex, columnIndex)} style={tileStyle}>
      <span style={circleStyle}></span>
    </button>
  )
}

export default Tile
