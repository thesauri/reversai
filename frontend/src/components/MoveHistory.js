import React from 'react'

const MoveHistory = ({ history }) => {
  return (
    <div style={{margin: '10px', display: 'grid'}}>
      <div style={{gridColumnStart: '1'}}>Move</div>
      <div style={{gridColumnStart: '2'}}>Time</div>
      {history.map((move, i) => (
        <>
          <div style={{gridColumnStart: '1'}}>{move.move[0]}, {move.move[1]}</div>
          <div style={{gridColumnStart: '2'}}>{move.time}</div>
        </>
      ))}
    </div>
  )
}

export default MoveHistory
