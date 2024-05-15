let currentGame = 1;

function nextGameUI() {
    currentGame = currentGame % 5 + 1;
    for (let i = 1; i <= 5; i++) {
        const elem = document.getElementById(`game${i}`)
        elem.style.display = (i == currentGame) ? 'block' : 'none';       
    }
}

function appendText(selector) {
    console.log('append text called')
    console.log(this.event.target.textContent)
    document.querySelector(selector).value += this.event.target.textContent
}

function setupWebsocketConnection() {

    const ws = new WebSocket(`ws://${window.location.host}/ws${window.location.pathname}`)

    ws.addEventListener('open', () => console.log('connected'))
    ws.addEventListener('message', msg => {
        const {type, data} = JSON.parse(msg.data)
        console.log(type, data)
        switch (type) {
        case 'update_ui':
            for (const [id, textContent] of Object.entries(data)) {
                console.log(id, textContent)
                document.getElementById(id).textContent = textContent
            }
            break
        case 'update_timer':
            document.querySelector('#timer').textContent = data.value
            break
        }
    })
    return ws
}

function setupGame1Listeners(ws) {
    document.querySelector('#game1-answer').onkeyup = e => {
        if (e.key === 'Enter') {
            document.querySelector('#submit').click()
        }
    }

    document.querySelector('#game1-submit').onclick = (e) => {
        e.preventDefault()
        const answer = document.querySelector('#game1-answer').value
        const msg = {
            'type': 'game1-answer',
            answer
        }
        ws.send(JSON.stringify(msg))
    }
}

function setupTimer(ws) {
    const timerIntervalId = setInterval(() => {
        const timer = document.querySelector('#timer')
        timer.textContent -= 1
        if (parseInt(timer.textContent) == -1) {
            ws.send(JSON.stringify({
                'type': 'time_ran_out'
            }))
            clearInterval(timerIntervalId)
        }
    }, 1000)
}

function main() {
    const ws = setupWebsocketConnection();
    setupTimer(ws);
    setupGame1Listeners(ws);
}

main()