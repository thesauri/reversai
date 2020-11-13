import React, { useState } from 'react'
import './App.css';
import Reversi from './components/Reversi'
import PlayerInfo from './components/PlayerInfo'
import TournamentInfo from './components/TournamentInfo'
import Banner from './components/Banner'
import { useWsApi } from './services/websocket'

function App() {
  const [currentPlayer, setCurrentPlayer] = useState('white')
  const [board, setBoard] = useState(null)
  const [latestPosition, setLatestPosition] = useState([null,null])
  const [winner, setWinner] = useState('')
  const [players, setPlayers] = useState({
    white: { name: 'Human', author: '' },
    black: { name: 'Human', author: '' }
  })
  const [matchHistory, setMatchHistory] = useState([])
  const [groups, setGroups] = useState([])

  const handleBoardEvent = ({
    matchHistory,
    groups,
    intermediateBoard,
    newBoard,
    turn,
    latestPosition,
    winner,
    black,
    white,
  }) => {
    if (matchHistory) {
      setMatchHistory(matchHistory)
      setGroups(groups)
    }
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
    } 
    if (newBoard) {
      setBoard(newBoard)
      setCurrentPlayer(turn)
      setPlayers({
        white: white || { name: 'Human', author: 'God' },
        black: black || { name: 'Human', author: 'God' }
      })
    }
  }
  
  const handleClick = (rowIndex, columnIndex) => {
    sendEvent({rowIndex, columnIndex})
  }

  const [onBoardUpdate, sendEvent] = useWsApi()
  onBoardUpdate.current = handleBoardEvent

  return (
    <div style={{display: 'grid'}}>
      <Banner />
      <div style={{width: '576px', gridColumnStart: '1'}}>
        <Reversi
        board={board}
        handleClick={handleClick}
        currentPlayer={currentPlayer}
        latestPosition={latestPosition}
        winner={winner}
        />
        <PlayerInfo
          winner={winner}
          currentPlayer={currentPlayer}
          players={players}
        />
      </div>
      <div style={{gridArea: '2 / 2 / 2 / 5'}}>
        <TournamentInfo matchHistory={matchHistory} groups={groups}/>
      </div>
    </div>
  );
}

export default App



