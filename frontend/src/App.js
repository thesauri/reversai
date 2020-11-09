import React, { useState } from 'react'
import './App.css';
import Reversi from './components/Reversi'
import PlayerInfo from './components/PlayerInfo'
import { useWsApi } from './services/websocket'

function App() {
  const [currentPlayer, setCurrentPlayer] = useState('white')
  const [board, setBoard] = useState(null)
  const [latestPosition, setLatestPosition] = useState([null,null])
  const [winner, setWinner] = useState('')

  const countPieces = () => {
    return {
      white: board.count('white'),
      black: board.count('black')
    }
  }

  const handleBoardEvent = ({
    intermediateBoard,
    newBoard,
    turn,
    latestPosition,
    winner
  }) => {
    if (latestPosition) {
      setLatestPosition(latestPosition)
    }
    if (winner) {
      setWinner(winner)
    }
    if (intermediateBoard) {    
      setBoard(intermediateBoard)
      setTimeout(() => {
        setBoard(newBoard)
        setCurrentPlayer(turn)
      }, 300)
    } else {
      setBoard(newBoard)
      setCurrentPlayer(turn)
    }
  }
  
  const handleClick = (rowIndex, columnIndex) => {
    sendEvent({rowIndex, columnIndex})
  }

  const [onBoardUpdate, sendEvent] = useWsApi()
  onBoardUpdate.current = handleBoardEvent

  return (
    <div>
      <div style={{width: '576px'}}>
        <Reversi
        board={board}
        handleClick={handleClick}
        currentPlayer={currentPlayer}
        latestPosition={latestPosition}
        winner={winner}
        />
        <PlayerInfo winner={winner} currentPlayer={currentPlayer}/>
      </div>
    </div>
  );
}

export default App



