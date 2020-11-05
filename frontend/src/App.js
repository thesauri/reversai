import React, { useState, useEffect } from 'react'
import './App.css';
import Reversi from './components/Reversi'
import PlayerInfo from './components/PlayerInfo'

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

  useEffect(() => {
    const url = 'ws://localhost:6666'
    const socket = new WebSocket(url)

    socket.onmessage = (event) => {
      const newBoard = JSON.parse(event.data)
      setBoard(newBoard)
    }
  }, [])

  return (
    <div style={{width: '576px'}}>
      <Reversi
      board={board}
      setBoard={setBoard}
      currentPlayer={currentPlayer}
      setCurrentPlayer={setCurrentPlayer}
      />
      <PlayerInfo currentPlayer={currentPlayer}/>
    </div>
  );
}

export default App;
