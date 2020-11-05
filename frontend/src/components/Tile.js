import React from 'react'

const Tile = ({ 
  tile,
  rowIndex,
  columnIndex
}) => {
  const style = {
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
    webkitAppearance: 'none',
    mozAppearance: 'none',
  }
  const circleStyle = {
    height: '3.5rem',
    width: '3.5rem',
    position: 'relative',
    //right: '8px',
    borderRadius: '50%',
    display: 'inline-block',
  }

  if (tile === 'white') {
    circleStyle.backgroundColor = 'white'
  } else if (tile === 'black') {
    circleStyle.backgroundColor = 'black'
  } else {
    style.cursor = 'pointer'
  }

  return (
    <button style={style}>
      <span style={circleStyle}></span>
    </button>
  )
}

export default Tile
