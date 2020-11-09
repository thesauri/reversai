import React from 'react'
import logo from '../ReversAI.png';

const Banner = () => {
  const bannerStyle = {
    gridArea: '1 / 1 / 1 / 5',
    //textAlign: 'center',
    padding: '10px',
    background: '#ddd',
    borderBottom: '3px solid #ccc',
  }
  return (
    <div style={bannerStyle}>
      <img src={logo} alt="Logo" width='300px'/>
    </div>
  )
}

export default Banner