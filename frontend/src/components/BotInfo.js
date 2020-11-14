import React from 'react'
import { FaCaretUp, FaCaretDown } from 'react-icons/fa'

const BotInfo = ({ name, points, annotation, stripe, isPlaying }) => {
  const getAnnotation = (annotation) => {
    if (annotation) {
      return annotation === 'up' ?
      <FaCaretUp style={{color: 'green'}}/> :
      <FaCaretDown style={{color: 'red'}}/>
    } else {
      return ''
    }
  }

  return (
    <div style={{
      display: 'grid',
      width: '100%',
      backgroundColor: isPlaying ? "#e0923c" : (stripe ? 'white' : '#f0f0f0')
    }}>
      <div style={{
        gridColumnStart: '1',
        textAlign: 'left',
        width: '175px',
        overflow: 'hidden',
        paddingLeft: '15px',
        }}>
        {name} 
      </div>
      <div style={{
        gridColumnStart: '2',
        textAlign: 'right',
        width: '20px',
        }}>
          {getAnnotation(annotation)}
        
      </div>
      <div style={{
        gridColumnStart: '3',
        fontWeight: 'bold',
        textAlign: 'center',
        width: '40px',
        paddingRight: '15px',
        }}>
          {points}
      </div>
    </div>
  )
}

export default BotInfo
