import { useState, useEffect, useRef } from 'react'
import WS_URL from '../config';

export const useWsApi = (url) => {
  const socket = useRef(new WebSocket(WS_URL));
  const onBoardUpdate = useRef(() => {console.error('No function here yet')})
  const [readyState, setReadyState] = useState(WebSocket.CONNECTING);
  
  useEffect(() => {
    socket.current.addEventListener("open", () => {
      setReadyState(socket.current.readyState)
    })
    socket.current.addEventListener("close", () => {
      console.log('uh oh closed')
      setReadyState(socket.current.readyState)
    })
    socket.current.addEventListener("message", (event) => {
      const data = JSON.parse(event.data)
      onBoardUpdate.current(data)
    })
  }, [])

  const sendEvent = data => {
    if (!socket.current || socket.current.readyState !== WebSocket.OPEN) {
      console.error("Unable to send event: connection not open")
      return
    }
    const payload = JSON.stringify(data)
    console.log('payload', payload)
    socket.current.send(payload)
  }
  return [readyState, onBoardUpdate, sendEvent]
}