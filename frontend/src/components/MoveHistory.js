import React from 'react'

const Move = ({ player, position, time }) => {
  const style = {
    display: 'grid',
    width: '90%',
    padding: '0px 10px',
    textAlign: 'left',
    backgroundColor: player === 'white' ? '#fff' : '#99d3cb',
  }
  if (time > 5) {
    style.color = '#c73029'
    style.fontWeight = 'bold'
  }

  return (
    <div style={style}>
      <div style={{gridColumnStart: '1'}}>{player}</div>
      <div style={{gridColumnStart: '2'}}>{position}</div>
      <div style={{gridColumnStart: '3'}}>{Math.round(time * 10)/10}</div>
    </div>
  )
}

const MoveHistory = React.forwardRef(({ history }, ref) => {
  const style = {
    margin: '20px',
    height: '743px',
    width: '200px',
    overflow: 'scroll',
    background: '#white',
    boxShadow: '0px 5px 5px #aaa'
  }
  const headerStyle = {
    display: 'grid',
    width: '90%',
    padding: '10px',
    margin: '0px 0px 5px 0px',
    textAlign: 'left',
    fontWeight: 'bold',
    background: 'white',
  }

  return (
    <div style={style}>
      <div style={headerStyle}>
        <div style={{gridColumnStart: '1'}}>Player</div>
        <div style={{gridColumnStart: '2'}}>Move</div>
        <div style={{gridColumnStart: '3'}}>Time</div>
      </div>
      {history.filter(move => move.move).map((move) => {
        const position = `${move.move[0] + 1}, ${move.move[1] + 1}`
        return (
          <Move
            key={position}
            player={move.player}
            position={position}
            time={move.time}
          />
        )
      })}
      <div ref={ref}></div>
    </div>
  )
})

export default MoveHistory
