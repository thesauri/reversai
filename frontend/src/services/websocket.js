import { useEffect, useRef } from 'react'
import WS_URL from '../config';

export const useWsApi = (url) => {
  const socket = useRef(null)
  const onBoardUpdate = useRef(() => {console.error('No function here yet')})

  useEffect(() => {
    socket.current = new WebSocket(WS_URL)
    console.log('websocket created')
    socket.current.addEventListener("open", () => {
      console.log('Websocket connection opened')
    })
    socket.current.addEventListener("close", () => {
      console.log('Websocket connection closed')
    })
    socket.current.addEventListener("message", (event) => {
      const data = JSON.parse(event.data)
      onBoardUpdate.current(data)
      console.log('msg received', data)
    })
  }, [])

  const sendEvent = data => {
    if (!socket.current || socket.current.readyState !== WebSocket.OPEN) {
      console.error("Unable to send event: connection not open")
      return
    }
    const payload = JSON.stringify(data)
    socket.current.send(payload)
  }
  return [onBoardUpdate, sendEvent]
}