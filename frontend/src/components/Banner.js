import React from 'react'
import logo from '../ReversAI.png';

const Banner = () => {
  const bannerStyle = {
    gridArea: '1 / 1 / 1 / 3',
    //textAlign: 'center',
    padding: '20px',
    background: '#ddd',
    borderBottom: '3px solid #ccc',
  }
  return (
    <div style={bannerStyle}>
      <img src={logo} alt="Logo" width='500px'/>
    </div>
  )
}

export default Banner