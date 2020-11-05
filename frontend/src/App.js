import React, { useState } from 'react'
import './App.css';
import Reversi from './components/Reversi'
import PlayerInfo from './components/PlayerInfo'
import { useWsApi } from './services/websocket'

function App() {
  const mockBoard = [
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '','black','white', '', '', ''],
    ['', '', '','white','black', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
    ['', '', '', '', '', '', '', ''],
  ]

  const [currentPlayer, setCurrentPlayer] = useState('white')
  const [board, setBoard] = useState(mockBoard)

  const handleBoardEvent = ({ board, turn }) => {
    setBoard(board)
    setCurrentPlayer(turn)
  }

  const getOtherPlayer = player => {
    return player === 'black' ? 'white' : 'black'
  }

  const handleClick = (rowIndex, columnIndex) => {
    sendEvent({rowIndex, columnIndex})
  }

  const [readyState, onBoardUpdate, sendEvent] = useWsApi()
  onBoardUpdate.current = handleBoardEvent

  return (
    <div style={{width: '576px'}}>
      <Reversi
      board={board}
      handleClick={handleClick}
      />
      <PlayerInfo currentPlayer={currentPlayer}/>
    </div>
  );
}

export default App



