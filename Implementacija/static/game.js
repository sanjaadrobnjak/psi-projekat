const game1Submit = document.querySelector('#game1-submit')
const game1Answer = document.querySelector('#game1-answer')
const timer = document.querySelector('#timer')

let currentRow=0;
let currentTile=0;

function showGameUI(ui,isActive, ws) {
    for (let i = 1; i <= 5; i++) {
        const currentUI = `game${i}`
        const elem = document.getElementById(currentUI)
        elem.style.display = (ui == currentUI) ? 'block' : 'none';       
    }
    if (ui == 'game1') {
        game1Submit.disabled = false
        game1Answer.value = ''
        timer.textContent = 60
    }
    if (ui=='game3'){
        //document.getElementById('current-player').style.display = 'none';
        const buttons = document.querySelectorAll(`#${ui} button`);
        buttons.forEach(button => {
            button.disabled = !isActive;
        });
       
        //initializeBoard();
        

        if (isActive) {
            removeGame3Listeners(); //uklanja stare slusaoce dogadjaja
            setupGame3Listeners(ws);//postavlja nove slusaoce dogadjaja
        }else{
            removeGame3Listeners();//uklanja slusaoce dogadjaja kada je protivnik na potezu
        }
        
    }
}

initializeBoard();


function initializeBoard(){
    //currentRow=0;
    //currentTile=0;
    const board = document.getElementById('board');

    
    board.innerHTML = ''; // Očisti prethodne elemente ako postoje
    

    for (let i = 0; i < 7; i++) {
        for (let j = 0; j < 5; j++) {
            const tileId = `tile-${i}-${j}`;
            if (!document.getElementById(tileId)) {
                const tile = document.createElement('div');
                tile.id = tileId;
                tile.className = 'tile';
                board.appendChild(tile);
            }
        }
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
            showGameUI(ui, data.is_active, ws);
            for (const [id, textContent] of Object.entries(data)) {
                let elem=document.getElementById(id);
                if (elem) {
                    console.log(id, textContent);
                    elem.textContent = textContent;
                } else {
                    console.warn(`Element with id ${id} not found`);
                }
                //console.log(id, textContent)
                //document.getElementById(id).textContent = textContent;
            }
            break
        case 'update_timer':
            document.querySelector('#timer').textContent = data.value
            break
        case 'guess':
            handleGuess(data);
            break;
        case 'game3_key_input':
            handleKeyInput(data);
            break;
        }
    });
    return ws;
}

function handleKeyInput(data) {
    const { action, letter, row, tile } = data;
    const tileElement = document.getElementById(`tile-${row}-${tile}`);
    if (action === 'add') {
        tileElement.textContent = letter;
    } else if (action === 'delete') {
        tileElement.textContent = '';
    }
}

function setupGame1Listeners(ws) {
    game1Answer.addEventListener('keydown', e => {
        if (e.key === 'Enter') {
            game1Submit.click()
            return
        }
        if (e.ctrlKey || e.altKey || typeof e.key !== 'string' || e.key.length != 1) {
            return
        }
        if (!'0123456789+-*/() '.includes(e.key)) {
            e.preventDefault()
        }
    }, false)

    game1Submit.onclick = (e) => {
        e.preventDefault()
        game1Submit.disabled = true;
        const msg = {
            'type': 'game1_answer',
            'answer': game1Answer.value
        }
        ws.send(JSON.stringify(msg))
    }

    game1Answer.focus()
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
            document.querySelector('#game2-submit').click()
        }
    }

    document.querySelector('#game2-submit').onclick = (e) => {
        e.preventDefault()

        let answerTime=new Date().getTime();
        let answerTimeDiv = document.getElementById('answer-time');
        answerTimeDiv.textContent = answerTime;
        const answer = document.querySelector('#game2-answer').value;
        const msg = {
            'type': 'game2_answer',
            answer,
            'answer_time':answerTime
        }
        ws.send(JSON.stringify(msg))
        document.getElementById("game2-answer").value="";
    }
}



function handleGuess(data){
    let feedback = data.feedback;
    let finished = data.finished;
    currentRow=data.currentRow;
    let player=data.player;
    

    let next_player;
    if(player=='blue') next_player='orange';
    else next_player='blue';

    for (let i = 0; i < feedback.length; i++) {
        const tileId = `tile-${currentRow}-${i}`;
        console.log("tileID je "+tileId);
        const tile = document.getElementById(tileId);
        const status = feedback[i];
        console.log("status mi je "+status);
        if (status === 'pogodjenoNaMestu') {
            tile.style.backgroundColor = '#1B6C8C';
        } else if (status === 'pogodjenoNijeNaMestu') {
            tile.style.backgroundColor = '#F2B441';
        } else {
            tile.style.backgroundColor = '#BF5B04';
        }
    }

    if (finished) { //igrac koji je na potezu pronasao rec
        console.log("Pogodjena rec "+data.targetWord+" u redu "+currentRow);
        setTimeout(() => {
            alert('Čestitamo! Pogodili ste reč!')
            resetBoard() // Resetuje ploču nakon završetka runde
        }, 100)
    } else {
        console.log("Nije pogodjena rec "+data.targetWord+" u redu "+currentRow)
        currentRow++;
        currentTile = 0;
        if (currentRow == 6) {
            console.log("igra je zavrsena za protivnika sa bojom "+player);
            if (player === 'blue') {    //napraviti da bude univerzalno 
                document.querySelectorAll('.keyboard button').forEach(button => button.disabled = true);
            } else {
                document.querySelectorAll('.opponent-keyboard button').forEach(button => button.disabled = false);
            }
        }
        if (currentRow==7){
            setTimeout(() => {
                alert('Igra je završena! Reč je bila ' + data.targetWord);
                resetBoard(); // Resetuje ploču nakon završetka runde
            }, 100);
        }
        
        
    }

}


function resetBoard() {
    for (let i = 0; i < 7; i++) {
        for (let j = 0; j < 5; j++) {
            const tile = document.getElementById(`tile-${i}-${j}`)
            tile.textContent = ''
            tile.style.backgroundColor = 'white' // Resetuje pozadinsku boju
        }
    }
    currentRow = 0
    currentTile = 0
}

/*function setupGame3Listeners(ws){
    document.querySelectorAll('.keyboard button').forEach(button => {
        button.addEventListener('click', (event) => handleInput(event.target.textContent, ws));
    });
    document.addEventListener('keydown', (event)=>handleKeyDown(event, ws));
}

function removeGame3Listeners() {
    document.querySelectorAll('.keyboard button').forEach(button => {
        button.removeEventListener('click', handleButtonClick);
    });

    document.removeEventListener('keydown', handleKeyDown);
}*/

let handleButtonClickReference = null;
let handleKeyDownReference = null;

function setupGame3Listeners(ws) {
    handleButtonClickReference = (event) => handleButtonClick(event, ws);
    handleKeyDownReference = (event) => handleKeyDown(event, ws);

    document.querySelectorAll('.keyboard button').forEach(button => {
        button.addEventListener('click', handleButtonClickReference);
    });
    document.addEventListener('keydown', handleKeyDownReference);
}

function removeGame3Listeners() {
    if (handleButtonClickReference) {
        document.querySelectorAll('.keyboard button').forEach(button => {
            button.removeEventListener('click', handleButtonClickReference);
        });
    }
    if (handleKeyDownReference) {
        document.removeEventListener('keydown', handleKeyDownReference);
    }
}


function handleButtonClick(event) {
    handleInput(event.target.textContent, ws);
}

function handleKeyDown(event, ws){  
    const key = event.key.toUpperCase();
    if (key === 'ENTER') {
        handleInput('Enter', ws);
    } else if (key === 'BACKSPACE') {
        handleInput('Delete', ws);
    } else if (key.match(/^[A-Z]$/)) {
        handleInput(key, ws);
    }
}

function handleInput(input, ws) {
    if (input === 'Enter') {
        if (currentTile === 5) {
            checkWord(ws);
            //currentRow++;
            //currentTile=0;
        }
    } else if (input === 'Delete') {
        deleteLetter(ws);
    } else {
        addLetter(input, ws);
    }
}

function addLetter(letter, ws) {
    if (currentTile < 5 && currentRow < 7) {
        const tile = document.getElementById(`tile-${currentRow}-${currentTile}`);
        tile.textContent = letter;
        currentTile++;

        ws.send(JSON.stringify({
            type: 'game3_key_input',
            data: {
                action: 'add',
                letter: letter,
                row: currentRow,
                tile: currentTile - 1
            }
        }));
    }
}

function deleteLetter(ws) {
    if (currentTile > 0) {
        currentTile--;
        const tile = document.getElementById(`tile-${currentRow}-${currentTile}`);
        tile.textContent = '';

        ws.send(JSON.stringify({
            type: 'game3_key_input',
            data: {
                action: 'delete',
                row: currentRow,
                tile: currentTile
            }
        }));
    }
}

function checkWord(ws) {
    let guessedWord = '';
    for (let i = 0; i < 5; i++) {
        guessedWord += document.getElementById(`tile-${currentRow}-${i}`).textContent;
    }
    guessedWord = guessedWord.toUpperCase();
    console.log("poslata je rec "+guessedWord);

    ws.send(JSON.stringify({
        type: 'game3_answer',
        word: guessedWord,
        attempts: currentRow + 1
    }));
}

function main() {
    const ws = setupWebsocketConnection();
    setupTimer(ws);
    setupGame1Listeners(ws);
    setupGame2Listeners(ws);
    //setupGame3Listeners(ws);
    if (document.getElementById('game3').style.display === 'block') {
        setupGame3Listeners(ws);
        initializeBoard();
    }

    
}

main()
