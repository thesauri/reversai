import React from 'react'
import { FaCaretUp, FaCaretDown } from 'react-icons/fa'

const BotInfo = ({ name, points, annotation, stripe }) => {
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
    <div style={{display: 'grid', textAlign: 'center', margins: 'auto', backgroundColor: stripe ? 'white' : '#f0f0f0'}}>
      <div style={{
        gridColumnStart: '1',
        textAlign: 'right'
        }}>
        {name} 
      </div>
      <div style={{
        gridColumnStart: '2',
        fontWeight: 'bold',
        textAlign: 'center',
        }}>
        {points}  
      </div>
      <div style={{
        gridColumnStart: '3',
        textAlign: 'left',
        }}>
      {getAnnotation(annotation)}
      </div>
    </div>
  )
}

export default BotInfo
