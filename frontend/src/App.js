import React, { useState } from 'react'
import './App.css';
import Reversi from './components/Reversi'
import PlayerInfo from './components/PlayerInfo'
import TournamentInfo from './components/TournamentInfo'
import Banner from './components/Banner'
import { useWsApi } from './services/websocket'
import MoveHistory from './components/MoveHistory'

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
  const [moveHistory, setMoveHistory] = useState([])

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
    deltaTime,
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
      setMoveHistory(moveHistory.concat(
        {move: latestPosition, time: deltaTime, player: turn === 'white' ? 'black' : 'white'}))
    } 
    if (newBoard) {
      setBoard(newBoard)
      setCurrentPlayer(turn)
    }
    if (!intermediateBoard && !matchHistory) {
      setPlayers({
        white: white || { name: 'Human', author: 'God' },
        black: black || { name: 'Human', author: 'God' }
      })
      setMoveHistory([])
      setWinner('')
      setLatestPosition([null,null])
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
      <div style={{gridArea: '2 / 2 / 2 / 2', textAlign: 'left'}}>
          <MoveHistory history={moveHistory} />
        </div>
      <div style={{gridArea: '3 / 2 / 3 / 5'}}>
        <TournamentInfo matchHistory={matchHistory} groups={groups}/>
      </div>
    </div>
  );
}

export default App



