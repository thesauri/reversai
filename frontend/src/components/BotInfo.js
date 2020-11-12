import React from 'react'

const BotInfo = ({ name, points, annotation }) => {
  return (
    <li>
      {name} {points} {annotation ? annotation : ''}
    </li>
  )
}

export default BotInfo
