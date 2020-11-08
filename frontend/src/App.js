import React, { useState } from 'react'
import './App.css';
import Reversi from './components/Reversi'
import PlayerInfo from './components/PlayerInfo'
import { useWsApi } from './services/websocket'

function App() {
  const [currentPlayer, setCurrentPlayer] = useState('white')
  const [board, setBoard] = useState(null)

  const handleBoardEvent = ({ intermediateBoard, newBoard, turn }) => {
    if (intermediateBoard) {
      setBoard(intermediateBoard)
      setTimeout(() => {
        setBoard(newBoard)
        setCurrentPlayer(turn)
      }, 1000)
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
        />
        <PlayerInfo currentPlayer={currentPlayer}/>
      </div>
    </div>
  );
}

export default App



