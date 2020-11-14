import React, { useState, useEffect, useRef } from 'react'
import './App.css';
import Reversi from './components/Reversi'
import PlayerInfo from './components/PlayerInfo'
import TournamentInfo from './components/TournamentInfo'
import Banner from './components/Banner'
import { useWsApi } from './services/websocket'
import MoveHistory from './components/MoveHistory'

function App() {
  const mockGames = [] //[{'white': {'score': 16, 'name': 'Pikachu'}, 'black': {'score': 48, 'name': 'Squirtle'}}, {'white': {'score': 23, 'name': 'Pikachu'}, 'black': {'score': 41, 'name': 'Dratini'}}, {'white': {'score': 12, 'name': 'Pikachu'}, 'black': {'score': 52, 'name': 'Meowth'}}, {'white': {'score': 35, 'name': 'Squirtle'}, 'black': {'score': 29, 'name': 'Dratini'}}, {'white': {'score': 50, 'name': 'Squirtle'}, 'black': {'score': 14, 'name': 'Meowth'}}, {'white': {'score': 43, 'name': 'Dratini'}, 'black': {'score': 21, 'name': 'Meowth'}}, {'white': {'score': 37, 'name': 'Psyduck'}, 'black': {'score': 27, 'name': 'Charmander'}}, {'white': {'score': 13, 'name': 'Psyduck'}, 'black': {'score': 51, 'name': 'Bulbasaur'}}, {'white': {'score': 48, 'name': 'Psyduck'}, 'black': {'score': 16, 'name': 'Eevee'}}, {'white': {'score': 38, 'name': 'Charmander'}, 'black': {'score': 26, 'name': 'Bulbasaur'}}, {'white': {'score': 33, 'name': 'Charmander'}, 'black': {'score': 31, 'name': 'Eevee'}}, {'white': {'score': 34, 'name': 'Bulbasaur'}, 'black': {'score': 30, 'name': 'Eevee'}}, {'white': {'score': 23, 'name': 'Pikachu'}, 'black': {'score': 41, 'name': 'Squirtle'}}, {'white': {'score': 17, 'name': 'Pikachu'}, 'black': {'score': 47, 'name': 'Dratini'}}, {'white': {'score': 43, 'name': 'Pikachu'}, 'black': {'score': 21, 'name': 'Meowth'}}, {'white': {'score': 42, 'name': 'Squirtle'}, 'black': {'score': 22, 'name': 'Dratini'}}, {'white': {'score': 21, 'name': 'Squirtle'}, 'black': {'score': 43, 'name': 'Meowth'}}, {'white': {'score': 28, 'name': 'Dratini'}, 'black': {'score': 36, 'name': 'Meowth'}}, {'white': {'score': 41, 'name': 'Psyduck'}, 'black': {'score': 23, 'name': 'Charmander'}}, {'white': {'score': 21, 'name': 'Psyduck'}, 'black': {'score': 43, 'name': 'Bulbasaur'}}, {'white': {'score': 29, 'name': 'Psyduck'}, 'black': {'score': 35, 'name': 'Eevee'}}, {'white': {'score': 10, 'name': 'Charmander'}, 'black': {'score': 54, 'name': 'Bulbasaur'}}, {'white': {'score': 33, 'name': 'Charmander'}, 'black': {'score': 31, 'name': 'Eevee'}}, {'white': {'score': 36, 'name': 'Bulbasaur'}, 'black': {'score': 28, 'name': 'Eevee'}}, {'white': {'score': 44, 'name': 'Pikachu'}, 'black': {'score': 20, 'name': 'Squirtle'}}, {'white': {'score': 38, 'name': 'Pikachu'}, 'black': {'score': 26, 'name': 'Dratini'}}, {'white': {'score': 17, 'name': 'Pikachu'}, 'black': {'score': 47, 'name': 'Meowth'}}, {'white': {'score': 23, 'name': 'Squirtle'}, 'black': {'score': 41, 'name': 'Dratini'}}, {'white': {'score': 29, 'name': 'Squirtle'}, 'black': {'score': 35, 'name': 'Meowth'}}, {'white': {'score': 46, 'name': 'Dratini'}, 'black': {'score': 18, 'name': 'Meowth'}}, {'white': {'score': 30, 'name': 'Psyduck'}, 'black': {'score': 34, 'name': 'Charmander'}}, {'white': {'score': 10, 'name': 'Psyduck'}, 'black': {'score': 54, 'name': 'Bulbasaur'}}, {'white': {'score': 11, 'name': 'Psyduck'}, 'black': {'score': 53, 'name': 'Eevee'}}, {'white': {'score': 50, 'name': 'Charmander'}, 'black': {'score': 14, 'name': 'Bulbasaur'}}, {'white': {'score': 22, 'name': 'Charmander'}, 'black': {'score': 42, 'name': 'Eevee'}}, {'white': {'score': 50, 'name': 'Bulbasaur'}, 'black': {'score': 14, 'name': 'Eevee'}}]
  const mockGroups = [] //[['Pikachu', 'Squirtle', 'Dratini', 'Meowth'], ['Psyduck', 'Charmander', 'Bulbasaur', 'Eevee']]
  const [currentPlayer, setCurrentPlayer] = useState('white')
  const [board, setBoard] = useState(null)
  const [latestPosition, setLatestPosition] = useState([null,null])
  const [winner, setWinner] = useState('')
  const [players, setPlayers] = useState({
    white: { name: 'Human', author: '' },
    black: { name: 'Human', author: '' }
  })
  const [matchHistory, setMatchHistory] = useState(mockGames)
  const [groups, setGroups] = useState(mockGroups)
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
      }, 1)
      setMoveHistory(moveHistory.concat(
        {move: latestPosition, time: deltaTime, player: turn === 'white' ? 'black' : 'white'}))
    } else if (newBoard) {
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

  // Used for autoscrolling movelist to bottom
  const bottomRef = useRef()
  useEffect(() => {
    if (bottomRef.current !== undefined) {
      bottomRef.current.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      })
    }
  }, [moveHistory])

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
      <div style={{gridArea: '2 / 2 / 2 / 2'}}>
          <MoveHistory history={moveHistory} ref={bottomRef}/>
        </div>
      <div style={{gridArea: '2 / 3 / 2 / 5'}}>
        <TournamentInfo matchHistory={matchHistory} groups={groups}/>
      </div>
    </div>
  );
}

export default App



