import React, {useRef} from 'react'

const Move = ({ player, position, time }) => {
  const style = {
    display: 'grid',
    width: '90%',
    padding: '0px 10px',
    textAlign: 'left',
    backgroundColor: player === 'white' ? '#fff' : '#99d3cb',
  }
  if (time > 10) {
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
    margin: '10px',
    padding: '10px 0px',
    height: '695px',
    width: '200px',
    overflow: 'scroll',
    background: 'white',
  }
  const headerStyle = {
    display: 'grid',
    width: '90%',
    padding: '0px 10px',
    textAlign: 'left',
    fontWeight: 'bold',
    borderBottom: '1px solid black'
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
