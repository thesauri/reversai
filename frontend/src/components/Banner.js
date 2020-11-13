import React from 'react'
import logo from '../reversai.svg';
import './Gradient.css'

const Banner = () => {
  const bannerStyle = {
    gridArea: '1 / 1 / 1 / 5',
    //textAlign: 'center',
    padding: '5px 0px 0px 150px',
    //background: '#ddd',
  }
  const gradientStyle = {
    position: 'absolute',
    top: '0px',
    left: '0px',
    width: '100%',
    height: '55px',
    zIndex: '-1',
  }

  return (
    <div>
      <div style={bannerStyle}>
        <img src={logo} alt="Logo" height='70px'/>
      </div>
      <div className='reversai-gradient' style={gradientStyle}></div>
    </div>
  )
}

export default Banner