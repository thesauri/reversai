import React, { useState } from 'react'
import './App.css';
import Othello from './components/Othello'

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
  const [board, setBoard] = useState(mockBoard)

  return (
    <div>
      <Othello board={board}/>
    </div>
  );
}

export default App;
