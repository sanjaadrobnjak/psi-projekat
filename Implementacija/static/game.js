function showGameUI(ui) {
    for (let i = 1; i <= 5; i++) {
        const currentUI = `game${i}`
        const elem = document.getElementById(currentUI)
        elem.style.display = (ui == currentUI) ? 'block' : 'none';       
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
        const {type, data, ui} = JSON.parse(msg.data)
        console.log(type, data, ui)
        switch (type) {
        case 'update_ui':
            showGameUI(ui)
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
            'type': 'game1_answer',
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

function setupGame2Listeners(ws) {
    document.querySelector('#game2-answer').onkeyup = e => {
        if (e.key === 'Enter') {
            document.querySelector('#submit').click()
        }
    }

    document.querySelector('#game2-submit').onclick = (e) => {
        e.preventDefault()

        let answerTime=new Date().getTime();
        let answerTimeDiv = document.getElementById('answer-time');
        answerTimeDiv.textContent = answerTime;
        const answer = document.querySelector('#game2-answer').value
        const msg = {
            'type': 'game2_answer',
            answer,
            'answer_time':answerTime
        }
        ws.send(JSON.stringify(msg))
    }
}


function main() {
    const ws = setupWebsocketConnection();
    setupTimer(ws);
    setupGame1Listeners(ws);
    setupGame2Listeners(ws);
}

main()