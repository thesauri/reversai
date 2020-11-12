const address = process.env.REACT_APP_IP || 'localhost'
const WS_URL = `ws://${address}:8008`
console.log('aaa', WS_URL)
export default WS_URL