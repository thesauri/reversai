import React, { useState } from 'react'
import './App.css';
import Othello from './components/Othello'
import PlayerInfo from './components/PlayerInfo'

function App() {
  const [currentPlayer, setCurrentPlayer] = useState('white')

  return (
    <div style={{width: '576px'}}>
      <Othello 
      currentPlayer={currentPlayer}
      setCurrentPlayer={setCurrentPlayer}
      />
      <PlayerInfo currentPlayer={currentPlayer}/>
    </div>
  );
}

export default App;
