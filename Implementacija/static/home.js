
document.getElementById('play-btn').addEventListener('click', function() {
    const prevContent = this.textContent
    this.textContent = "Traži se..."
    this.disabled = true
    const socket = new WebSocket(`ws://${window.location.host}/ws/lobby/`)

    socket.addEventListener('open', () => {
        console.log('Connection established')
    })

    socket.addEventListener('message', (e) => {
        const {gameUrl} = JSON.parse(e.data)
        window.location.href = gameUrl
    })
})

