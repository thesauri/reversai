import React, { useState } from 'react'
import './App.css';
import Reversi from './components/Reversi'
import PlayerInfo from './components/PlayerInfo'
import TournamentInfo from './components/TournamentInfo'
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
    matchHistory,
    groups,
    intermediateBoard,
    newBoard,
    turn,
    latestPosition,
    winner
  }) => {
    if (matchHistory) {
      return
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

  const matchHistory = [
    {
      black: {
        name: 'name1',
        score: 32,
      },
      white: {
        name: 'name2',
        score: 31,
      }
    },
    {
      black: {
        name: 'name3',
        score: 22,
      },
      white: {
        name: 'name4',
        score: 44,
      }
    },
    {
      black: {
        name: 'name1',
        score: 22,
      },
      white: {
        name: 'name2',
        score: 44,
      }
    },
    {
      black: {
        name: 'name1',
        score: 22,
      },
      white: {
        name: 'name2',
        score: 44,
      }
    },
  ]
  const groups = [['name1', 'name2'], ['name3', 'name4']]

  return (
    <div style={{display: 'grid'}}>
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
      <div>
        <TournamentInfo matchHistory={matchHistory} groups={groups}/>
      </div>
    </div>
  );
}

export default App



