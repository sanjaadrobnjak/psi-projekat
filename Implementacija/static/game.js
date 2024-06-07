/*
    Ivan Cancar 2021/0604,
    Sanja Drobnjak 2021/0492
    Luka Skoko 2021/0497
    Tanja Kvascev 2021/0031
*/ 

const game1Submit = document.querySelector('#game1-submit')
const game1Answer = document.querySelector('#game1-answer')
const timer = document.querySelector('#timer')

let currentRow=0;           //koristi se u trecoj igri, Paukova Sifra
let currentTile=0;          //koristi se u trecoj igri, Paukova sifra

let errors = 0;             //koristi se u petoj igri, Utekni pauku
const display_guessed_div = document.getElementById('display_guessed'); //koristi se u petoj igri, Utekni pauku

let game1AnswerSubmitted = false
let game2AnswerSubmitted=false;
let game3AnswerSubmitted=false;
let game4AnswerSubmitted=false;
let game5AnswerSubmitted=false;

/*
    prikazuje interfejs igre tako sto iterira kroz pet potencijalnih igara
    i prikazuje samo onu igru koja odgovara vrednosti ui dok ostale igre sakriva;
    ukoliko je ui jednako game3, funkcija omogucava dugmice i postavlja nove slusaoce dogadjaja 
    za trecu igru za jednog igraca, tj onemogucava dugmice i uklanja slusaoce dogadjaja za
    drugog igraca na osnovu vrednosti isActive
*/ 
function showGameUI(ui,isActive, ws) {
    for (let i = 1; i <= 5; i++) {
        const currentUI = `game${i}`
        const elem = document.getElementById(currentUI)
        elem.style.display = (ui == currentUI) ? 'block' : 'none';       
    }
    if (ui == 'game1') {
        game1Submit.disabled = false
        game1Answer.value = ''
        game1AnswerSubmitted = false
    }
    if(ui=='game2'){
        game2AnswerSubmitted=false;
    }
    if (ui=='game3'){
        game3AnswerSubmitted=false;
        //document.getElementById('current-player').style.display = 'none';
        const buttons = document.querySelectorAll(`#${ui} button`);
        buttons.forEach(button => {
            button.disabled = !isActive;
        });
       
        //initializeBoard();
        let playerMessage=document.getElementById('player-message');
        

        if (isActive) {
            playerMessage.textContent='Vi ste na potezu!';
            removeGame3Listeners(); //uklanja stare slusaoce dogadjaja
            setupGame3Listeners(ws);//postavlja nove slusaoce dogadjaja
        }else{
            playerMessage.textContent='Protivnik je na potezu, sačekajte svoj red!';
            removeGame3Listeners();//uklanja slusaoce dogadjaja kada je protivnik na potezu
        }
        
    }
    if(ui=='game4') {
        game4AnswerSubmitted = false;

        const buttons = document.querySelectorAll(`#${ui} button`); //
        buttons.forEach(button => {
            button.disabled = !isActive;
        });

        let playerMessage=document.getElementById('player-message4');
        if (isActive) {
            playerMessage.textContent='Vi ste na potezu!';
            removeGame4Listeners();
            setupGame4Listeners(ws);
        }else{
            playerMessage.textContent='Protivnik je na potezu, sačekajte svoj red!';
            removeGame4Listeners();
        }
    }
    if (ui=='game5'){
        game5AnswerSubmitted=false;

        const buttons = document.querySelectorAll(`#${ui} button`);
        buttons.forEach(button => {
            button.disabled = !isActive;
        });
       
        let playerMessage2=document.getElementById('player-message2');
        
        if (isActive) {
            playerMessage2.textContent='Vi ste na potezu!';
            removeGame5Listeners(); //uklanja stare slusaoce dogadjaja
            setupGame5Listeners(ws);//postavlja nove slusaoce dogadjaja
        }else{
            playerMessage2.textContent='Protivnik je na potezu, sačekajte svoj red!';
            removeGame5Listeners();//uklanja slusaoce dogadjaja kada je protivnik na potezu
        }
    }
}

initializeBoard();  //inicijalizuje se jednom na pocetku igre, za trecu igru Paukova Sifra
// ToDo: iniucijalizacija table za igru 4
// ToDo: onClick za buttone
initializeBoard2(); //inicijalizuje se jednom na pocetku igre, za petu igru Utekni pauku

function appendText(selector) {
    console.log('append text called')
    console.log(this.event.target.textContent)
    document.querySelector(selector).value += this.event.target.textContent
}

/*
    povezuje se na WebSocket server koristeci trenutnu lokaciju;
    kada stigne poruka parsira je iz JSON formata i prema tipu poruke-type obavlja razlicite akcije:
    ♥update_ui-prikazuje odgovarajuci interfejs igre pomocu funkcije showGameUI i azurira tekstualni 
    sadrzaj elemenata na osnovu pristiglih podataka
    ♥update_timer-azurira prikaz tajmera na osnovu pristigle vrednosti
    ♥guess-obradjuje podatak u trecoj igri pomocu funkcije handleGuess
    ♥guess2-obradjuje podatak u petoj igri pomocu funkcije handleGuess2
    ♥game3_key_input-rukuje unosom tastera za trecu igru pomocu funkcije handleKeyInput
    ♥end_turn_update-azurira interfejs i dostupnost dugmadi u slucaju da je sedmi pokusaj na redu
    ♥end_turn_update2-azurira interfejs i dostupnost dugmadi u slucaju da je sedmi pokusaj na redu
    ♥redirect-preusmerava korisnika na novu putanju na osnovu pristigle vrednosti pathname
    funkcija vraca WebSocket objekat ws
*/ 
function setupWebsocketConnection() {

    const ws = new WebSocket(`ws://${window.location.host}/ws${window.location.pathname}`)

    ws.addEventListener('open', () => console.log('connected'))
    ws.addEventListener('message', msg => {
        const {type, data, ui, pathname} = JSON.parse(msg.data)
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
            }
            break
        case 'update_timer':
            document.querySelector('#timer').textContent = data.value
            break
        case 'guess':
            handleGuess(data, ws);
            break;
        case 'guess2':
            handleGuess2(data, ws);
            break;
        case 'game3_key_input':
            handleKeyInput(data);
            break;
        // !!!
        // case 'game4_key_input':
        //     handle4KeyInput(data);
        //     break;
        case 'end_turn_update':
            console.log("Sedmi pokusaj je na redu");
            const buttons = document.querySelectorAll(`#${ui} button`);
            buttons.forEach(button => {
                button.disabled = !data.is_active;
            });
        
            let playerMessage=document.getElementById('player-message');
            
            if (data.is_active) {
                console.log("protivnicki igrac sme da upisuje");
                playerMessage.textContent='Vi ste na potezu!';
                removeGame3Listeners(); //uklanja stare slusaoce dogadjaja
                setupGame3Listeners(ws);//postavlja nove slusaoce dogadjaja
            }else{
                playerMessage.textContent='Protivnik je na potezu, sačekajte svoj red!';
                removeGame3Listeners();//uklanja slusaoce dogadjaja kada je protivnik na potezu
            }
            break;
        case 'end_turn_update4':
            console.log("kraj runde");
            const buttons4 = document.querySelectorAll(`#${ui} button`);
            buttons4.forEach(button => {
                button.disabled = !data.is_active;
            });
            let playerMessage4=document.getElementById('player-message4');

            if (data.is_active || attempts == 10) {
                console.log("protivnicki igrac sme da upisuje u igri 4");
                playerMessage4.textContent='Vi ste na potezu!';
                removeGame4Listeners();
                setupGame4Listeners(ws);
            }else{
                playerMessage4.textContent='Protivnik je na potezu, sačekajte svoj red!';
                removeGame4Listeners();
            }
            break;

        case 'end_turn_update2':
            console.log("Sedmi pokusaj");
            const buttons2 = document.querySelectorAll(`#${ui} button`);
            buttons2.forEach(button => {
                button.disabled = !data.is_active;
            });
        
            let playerMessage2=document.getElementById('player-message2');
            errors = 7;
            if (data.is_active) {
                console.log("protivnicki igrac sme da upisuje");
                playerMessage2.textContent='Vi ste na potezu!';
                removeGame5Listeners(); //uklanja stare slusaoce dogadjaja
                setupGame5Listeners(ws);//postavlja nove slusaoce dogadjaja
            }else{
                playerMessage2.textContent='Protivnik je na potezu, sačekajte svoj red!';
                removeGame5Listeners();//uklanja slusaoce dogadjaja kada je protivnik na potezu
            }
            break;
        case 'redirect':
            window.location.pathname = pathname
            break
        }
    });
    return ws;
}

/*
    funkcija rukuje unosom tastera za igru i azurira sadrzaj odredjenog polja na osnovu akcije;
    prima podatak data koji predstavlja objekat koji sadrzi informacije o akciji, slovu, redu i koloni-polju;
    pronalazi se element sa id-jem na osnov rednog broja i kolone koji su dobijeni parsiranjem iz objekta data i 
    u zavisnosti od akcije (da li je add ili delete) na element se postavlja vrednost letter, odnosno
    brise se tekst u elementu
*/ 
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
        game1AnswerSubmitted = true
        const msg = {
            'type': 'game1_answer',
            'answer': game1Answer.value
        }
        ws.send(JSON.stringify(msg))
    }

    game1Answer.focus()
}

/*
    funkcija pokrece tajmer koji odbrojava i salje poruke kada vreme istekne
    za razlicite igre; ulazni parametar ws predstavlja WebSocket konekciju koja
    se koristi za slanje poruka serveru;
    funkcija radi tako sto postavlja interval koje se ponavlja svake sekunde, na 
    svako ponavljanje parsira se vrednost tajmera iz elementa timer i u zavisnosti od 
    broja moguce su sledece situacije:
    ♥ako je vrednost tajmera 0, funkcija prestaje sa daljim izvrsavanjem za taj interval
    ♥ako vrednost tajmera nije 0, smanjuje se vrednost za 1 i azurira se prikaz elementa timer
    ♥ako je vrednost tajmera 1 i odgovori za igre nisu poslati (u prve dve igre dugmici za potvrdu, 
    u trecoj igri ukoliko za sedmi pokusaj nije pritisnut enter, u cetvrtoj igri ukoliko nije odigran deseti potez),
    salje se poruka preko WebSocket-a sa tipom time_ran_out
*/ 
function setupTimer(ws) {
    setInterval(() => {
        const timerValue = parseInt(timer.textContent)
        if (timerValue === 0) {
            return
        }
        timer.textContent = (timerValue - 1).toString()
        if (timerValue === 1 && !game1AnswerSubmitted) {
            ws.send(JSON.stringify({
                'type': 'time_ran_out'
            }))
        }
        if(timerValue==1 && !game2AnswerSubmitted){
            console.log("saljem poruku da je isteklo vreme za drugu igru");
            ws.send(JSON.stringify({
                'type':'time_ran_out'
            }))
        }
        if(timerValue==1 && !game3AnswerSubmitted){
            console.log("saljem poruku da je isteklo vreme za trecu igru");
            ws.send(JSON.stringify({
                'type':'time_ran_out'
            }))
        }
        if(timerValue==1 && !game4AnswerSubmitted){
            console.log("saljem poruku da je isteklo vreme za cetvrtu igru");
            ws.send(JSON.stringify({
                'type':'time_ran_out'
            }))
        }
        if(timerValue==1 && !game5AnswerSubmitted){
            console.log("saljem poruku da je isteklo vreme za petu igru");
            ws.send(JSON.stringify({
                'type':'time_ran_out'
            }))
        }
    }, 1000)
}

/*
    postavlja dogadjaje za unos i slanje odgovora u drugoj igri, Skok na Mrezu;
    kao ulazni parametar prima ws, koji predstavlja WebSocket konekciju koja se koristi za slanje odgovora serveru;
    funkcija radi tako sto postavlja dogadjaj koji se detektuje kada korisnik pritisne taster enter, tj dugme za potvrdu;
    takodje, pamti se da je korisnik pritisnuo dugme za potvrdu, kao i trenutno vreme; 
    kreira se poruka za slanje serveru (salje se preko WebSocket konekcije) koja sadrzi odgovor uzet iz polja za odgovor i
    vreme odgovora;na kraju se samo brise vrednost u polju za odgovor nakon slanja
*/ 
function setupGame2Listeners(ws) {
    document.querySelector('#game2-answer').onkeyup = e => {
        if (e.key === 'Enter') {
            document.querySelector('#game2-submit').click()
        }
    }

    document.querySelector('#game2-submit').onclick = (e) => {
        e.preventDefault();
        game2AnswerSubmitted=true;
        console.log("game2AnswerSubmitted "+game2AnswerSubmitted);

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

/*
    inicijalizuje tablu igre tako sto kreira mrezu plocica od 7 redova i 5 kolona;
    prvo ocisti sve prethodno kreirane elemente unutar elementa sa id-em board, i
    zatim iterira kroz 7 redova i 5 kolona kreirajuci i dodavajuci div elemente za
    svaku plocicu ukoliko ta plocica vec ne postoji. Svaka plocica dobija jedinstveni id
    i klasu tile
*/ 
function initializeBoard(){
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

/*
    inicijalizuje tablu igre tako sto kreira osam praznih polja
    prvo ocisti sve prethodno kreirane elemente unutar elementa sa id-em board, i
    zatim iterira osam puta kreirajuci i dodavajuci div elemente za
    svako polje ukoliko to polje vec ne postoji. Svako polje dobija jedinstveni id
    i klasu position
*/ 
function initializeBoard2(){
    const board2 = document.getElementById('board2');
    board2.innerHTML = ''; // Očisti prethodne elemente ako postoje
    for (let i = 0; i < 8; i++) {
        const posId = `position-${i}`;
        if (!document.getElementById(posId)) {
            const newPos = document.createElement('div');
            newPos.id = posId;
            newPos.className = 'position';
            newPos.textContent = '*';
            board2.appendChild(newPos);
        }
    }
     
}

/*
    obradjuje povratne informacije nakon pogadjanja reci u trecoj igri Paukova Sifra,
    kao ulazne parametre prima data-objekat koji sadrzi povratne informacije i ws-WebSocket 
    konekciju koja se koristi za slanje poruka serveru;
    funkcija iterira kroz niz feedback (sadrzi povratne informacije o trenutno popunjenom redu)
    i azurira boju plocica na osnovu statusa. Ukoliko je igra zavrsena-igrac koji je na potezu je
    uspesno pogodio zadatu rec, resetuje se tabla kako bi bila spremna za narednu rundu.
    U suprotnom, prelazi se na naredni red i trenutno polje u redu se resetuje. Ukoliko je trenutni 
    red dostigao sesti pokusaj onemogucavaju se dugmici za unos slova i azurira se poruka koji je igrac na potezu,
    salje se poruka serveru da je red zavrsen. Ukoliko je trenutni red dostigao sedmi pokusaj to znaci
    da ni protivnicki igrac nije uspeo da pogodi zadatu rec i tabla se resetuje
*/
function handleGuess(data, ws){
    let feedback = data.feedback;
    let finished = data.finished;
    currentRow=data.currentRow;
    let player=data.player;
    
    /*let next_player;
    if(player=='blue') next_player='orange';
    else next_player='blue';*/

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
            resetBoard() // Resetuje tablu nakon zavrsetka runde
        }, 100)
    } else {
        console.log("Nije pogodjena rec "+data.targetWord+" u redu "+currentRow)
        currentRow++;
        currentTile = 0;
        if (currentRow == 6) {
            console.log("igra je zavrsena za protivnika sa bojom "+player);
            document.querySelectorAll('.keyboard button').forEach(button => button.disabled = true);
            const playerMessage = document.getElementById('player-message');
            playerMessage.textContent = 'Protivnik je na potezu, sačekajte svoj red!';
            ws.send(JSON.stringify({
                type: 'end_turn',
                player: player
            }));
            removeGame3Listeners(); // Uklanja slušaoce dogadjaja nakon sestog pokušaja  
        }
        if (currentRow==7){
            setTimeout(() => {
                resetBoard(); // Resetuje tablu nakon zavrsetka runde
            }, 100);
        }   
    }
}

/*
    funkcija resetuje tablu sa plocicama u trecoj igri Paukova Sifra tako sto
    azurira boje plocica na pocetne, brise slova iz plocica i azurira vrednosti koje
    prate trenutni red i trenutnu plocicu
*/
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

/*
    promenljive cuvaju reference na funkcije koje rukuju dogadjajima 
    pritisaka i klikova na tastere kako bi se obezbedilo ispravno postavljanje
    i uklanjanje osluskivaca
*/
let handleButtonClickReference = null;  
let handleKeyDownReference = null; 

/*
    postavlja slusaoce za klik dugmica i pristak na tastaturi u trecoj igri Paukova Sifra, 
    tako sto se najpre definisu fukcije handleButtonClickReference (poziva se kada se desi 
    klik dogadjaj na dugmicu i poziva funkciju handleButtonClick) i 
    Reference 
    (poziva se kada se desi prtisak na tastaturi i poziva handleKeyDown funkciju). Zatim se 
    dodaje dogadjaj klik za sve dugmice na ekranu koji ce pozvati handleButtonClickReference, 
    kao i dogadjaj za pritisak na tastaturi koji ce pozvati handleKeyDownReference
   
*/
function setupGame3Listeners(ws) {
    handleButtonClickReference = (event) => handleButtonClick(event, ws);
    handleKeyDownReference = (event) => handleKeyDown(event, ws);

    document.querySelectorAll('.keyboard button').forEach(button => {
        button.addEventListener('click', handleButtonClickReference);
    });
    document.addEventListener('keydown', handleKeyDownReference);
}

/*
    uklanja slusaoce dogadjaja koji su prethodno postavljeni u setupGame3Listeners. Funkcija
    radi tako sto se najpre proveri postojanje handleButtonClickReference i ukoliko postoji 
    selektuju se svi dugmici i sa njih se uklanja dogadjaj za klik na dugmice povezan sa 
    handleButtonClickReference. Potom, proverava se postojanje handleKeyDownReference i ako
    postoji uklanja se dogadjaj za pritisak na tastaturi povezan sa handleKeyDownReference
*/
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

/*
    poziva se kada korisnik pritisne dugme na ekranu,
    kao ulazne parametre prima event-dogadjaj koji se 
    desio i ws-WebSocket konekcija potrebna kao parametar 
    za handleInput funkciju;
    funkcija poziva funkciju handleInput sa tekstom dugmeta koje je kliknuto i ws kao argumentima
*/
function handleButtonClick(event, ws) {
    handleInput(event.target.textContent, ws);
}

/*
    poziva se kada korisnik pritisne taster na tastaturi,
    kao ulazne parametre prima event-dogadjaj koji se 
    desio i ws-WebSocket konekcija potrebna kao parametar 
    za handleInput funkciju;
    u zavisnosti od pritisnutog tastera poziva se funkcija handleInput sa tim tasterom i ws, kao parametrima
*/
function handleKeyDown(event, ws){  
    const key = event.key.toUpperCase();
    if (key === 'ENTER') {
        if (currentRow==6) game3AnswerSubmitted=true;
        handleInput('Enter', ws);
    } else if (key === 'BACKSPACE') {
        handleInput('Delete', ws);
    } else if (key.match(/^[A-Z]$/)) {
        handleInput(key, ws);
    }
}

/*
    obradjuje unos korisnika (dat kao prvi parametar input), 
    tako sto ukoliko je korisnik uneo enter, prvo se proverava da li je popunio sve plocice u redu i ukoliko jeste poziva se funkcija za proveru unete reci checkWord koja prima argument ws
    ukoliko korisnik uneo delete, poziva se funkcija za brisanje slova iz reda deleteLetter koja takodje prima ws
    i ukoliko je korisnik uneo neko slovo poziva se funkcija za postavljanje tog slova na trenutnu plocicu odnosno addLetter koja prima to slovo i ws kao argumente
*/
function handleInput(input, ws) {
    if (input === 'Enter') {
        if (currentTile === 5) {
            checkWord(ws);
        }
    } else if (input === 'Delete') {
        deleteLetter(ws);
    } else {
        addLetter(input, ws);
    }
}

/*
    dodaje slovo na trenutnu plocicu u trenutnom redu,
    kao parametre prima slovo koje unosi i WebSocket 
    konekciju za slanje poruke serveru,
    funkcija radi tako sto postavlja tekst slova na 
    trenutnu plocicu i salje poruku preko WebSocketa sa 
    informacijama o akciji dodavanja slova
*/
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

/*
    funkcija brise slovo sa trenutne plocice u trenutnom redu,
    kao ulazni parametar prima WebSocket konekciju za slanje poruke serveru,
    ukoliko postoji popunjene plocice u trenutnom redu, brise tekst iz nje i 
    salje poruku preko WebSocket-a sa informacijama o akciji brisanja slova
*/
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

/*
    funkcija proverava rec koju je korisnik uneo u trenutnom redu,
    kao ulazni parametar prima WebSocket konekciju za slanje poruke serveru,
    funkcija radi tako sto kreira rec od slova na plocicama u trenutnom redu i 
    salje rec preko WebSocket-a sa informacijama o unesenoj reci i broju pokusaja
*/
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


/*
function setupGame4Listeners(ws) {
    const buttons = document.querySelectorAll(".game4-container button");
    let firstSelected = null;

    buttons.forEach(button => {
        button.addEventListener('click', createHandleButtonClickReference4(ws));
    });
}

function removeGame4Listeners() {
    const buttons = document.querySelectorAll(".game4-container button");
    buttons.forEach(button => {
        button.removeEventListener("click", handleButtonClickReference4);
    });
}*/

const buttonListeners = [];
function setupGame4Listeners(ws) {
    const buttons = document.querySelectorAll(".game4-container button");

    buttons.forEach(button => {
        const listener = createHandleButtonClickReference4(ws); // , data ???
        buttonListeners.push({ button, listener });
        button.addEventListener('click', listener);
    });
}

function removeGame4Listeners() {
    buttonListeners.forEach(({ button, listener }) => {
        button.removeEventListener("click", listener);
    });
    buttonListeners.length = 0;
}


let firstSelectedButton = null;
let attempts = 0;
function createHandleButtonClickReference4(ws) { // , data ???
    return function handleButtonClickReference4(event) {
        const button = event.target;
        const id = parseInt(button.id);
        // let player=data.player;
        // errors=data.errors;
        // let finished = data.finished;


        // Ako je dugme iz leve kolone (id od 0 do 9)
        if (id >= 0 && id <= 9) {
            if (!firstSelectedButton) {
                // nema vec selektovano dugme (firstSelectedButton je null)
                button.classList.add('selected');
                firstSelectedButton = button;
            } else {
                // Ako je kliknuto drugo dugme iz leve kolone, resetuj selekciju na trenutno klinuto dugme
                firstSelectedButton.classList.remove('selected');
                button.classList.add('selected');
                firstSelectedButton = button;
            }
        }
        // Ako je dugme iz desne kolone (id od 10 do 19)
        else if (id >= 10 && id <= 19) {
            // pod uslovom da postiji vec selektovano dugme iz prve kolone mozemo da selektujemo i drugme iz druge kolone
            if (firstSelectedButton) {
                const firstId = parseInt(firstSelectedButton.id);

                // Provera ispravnosti para (drugo dugme mora imati ID tačno 10 veći od prvog)
                if (firstId + 10 === id) {
                    firstSelectedButton.classList.remove('selected');
                    firstSelectedButton.classList.add('matched');
                    button.classList.add('matched');
                } else {
                    firstSelectedButton.classList.remove('selected');
                    firstSelectedButton.classList.add('mismatched');
                    button.classList.add('mismatched');
                }

                // Povećanje broja pokušaja
                attempts++;

                // Ako je broj pokušaja dostigao 10, resetuj sve uz 10 sekunda kašnjenja pre resetovanja    
                const timerValue = parseInt(timer.textContent)        
                if (attempts == 10 || timerValue == 0) {
                    // resetovanje table nakon 1s nakon zavrsetka runde
                    setTimeout(() => {
                        resetBoard4();
                        game4AnswerSubmitted = true;
                    }, 1000); 

                    // prebacivanje na drugog protivnika
                    console.log("Partija cetvrte igre je zavrsena");
                    const playerMessage4 = document.getElementById('player-message4');
                    playerMessage4.textContent = 'Protivnik je na potezu, sačekajte svoj red!';

                    ws.send(JSON.stringify({
                        type: 'end_turn4',
                        // player: player
                    }));
                    removeGame4Listeners();
                }
                // Resetovanje selekcije za sledeći par
                firstSelectedButton = null;
            }
        }
    }
}

// Resetovanje table tako da bude spremna za narednu igru
function resetBoard4() {
    console.log("u1");
    document.querySelectorAll('.matched, .mismatched').forEach(btn => {
        console.log("u2");
        btn.classList.remove('matched', 'mismatched');
        btn.classList.remove('selected');
        // btn.disabled = false;
    });
    console.log("u3")
    attempts = 0;
}
    

/*
    obradjuje povratne informacije nakon pogadjanja reci ili slova u petoj igri Utekni pauku,
    kao ulazne parametre prima data-objekat koji sadrzi povratne informacije i ws-WebSocket 
    konekciju koja se koristi za slanje poruka serveru;
    funkcija iterira kroz niz feedback (sadrzi povratne informacije o tome da li je neko slovo pogodjeno ili ne)
    i azurira polja na osnovu toga. Ukoliko je igra zavrsena, a igrac koji je na potezu je
    uspesno pogodio zadatu rec, resetuje se tabla kako bi bila spremna za narednu rundu.
    U suprotnom, prelazi se na naredni pokusaj. 
    Ukoliko je trenutni igrac napravio sest gresaka onemogucavaju se dugmici za unos slova i azurira se poruka koji je igrac na potezu,
    salje se poruka serveru da je pokusaj tog igraca zavrsen. Ukoliko je broj gresaka dostigao sedam to znaci
    da ni protivnicki igrac nije uspeo da pogodi zadatu rec i tabla se resetuje
*/
function handleGuess2(data, ws){
    let feedback = data.feedback;
    let finished = data.finished;
    let arr = data.guessed_array
    errors=data.errors;
    let player=data.player;

    for (let i = 0; i < feedback.length; i++) {
        const posId = `position-${i}`;
        console.log("posID je " + posId);
        const position = document.getElementById(posId);
        const c = feedback[i];
        console.log("ovde je karakter " + c);
        if (c != '*') {
            position.textContent = c;
        } else {
            position.textContent = "*"
        }
    }

    display_guessed(`Prethodni pokušaji: ${arr.join(', ')}`);

    if (finished) { //igrac koji je na potezu pronasao rec
        console.log("Pogodjena rec "+data.targetWord+" uz "+ errors +" gresaka");
        setTimeout(() => {
            resetBoard2(); // Resetuje tablu nakon zavrsetka runde
        }, 100)
    } else {
        console.log("Nije pogodjena rec "+data.targetWord+" uz "+ errors +" gresaka")
        if (errors == 6) {
            console.log("igra je zavrsena za protivnika sa bojom "+player);
            document.querySelectorAll('.keyboard button').forEach(button => button.disabled = true);
            const playerMessage = document.getElementById('player-message2');
            playerMessage.textContent = 'Protivnik je na potezu, sačekajte svoj red!';
            ws.send(JSON.stringify({
                type: 'end_turn2',
                player: player
            }));
            removeGame5Listeners(); // Uklanja slušaoce dogadjaja nakon sestog pokušaja  
        }
        else if (errors==7){
            setTimeout(() => {
                resetBoard2(); // Resetuje tablu nakon zavrsetka runde
            }, 100);
        }   
    }
}

/*
    funkcija resetuje tablu sa poljima u petoj igri Utekni pauku tako sto
    brise slova iz polja, brise rec iz polja za unos reci i resetuje niz pogodjenih reci i slova
*/
function resetBoard2() {
    for (let i = 0; i < 8; i++) {
        const position = document.getElementById(`position-${i}`);
        position.textContent = '*';
    }
    errors = 0
    document.getElementById(`input_letter`).textContent = '';
    document.getElementById(`input_word`).value = '';
    document.getElementById(`display_guessed`).textContent = '';
}

/*
    promenljive cuvaju reference na funkcije koje rukuju dogadjajima 
    klikova na tastere kako bi se obezbedilo ispravno postavljanje
    i uklanjanje osluskivaca
*/
let handleLetterClickReference = null;  
let handleWordInputReference = null;  
let handleLetterInputReference = null;

/*
    funkcija sluzi za ispisivanje unetih reci i slova igraca u toj rundi
*/
function display_guessed(message){
    display_guessed_div.textContent = message;
}

/*
    postavlja slusaoce za klik dugmica u petoj igri UtekniPauku, 
    tako sto se najpre definisu fukcije handleLetterClickReference (poziva se kada se desi 
    klik dogadjaj na dugmicu i poziva funkciju handleLetterClick), handleLetterInputReference 
    (poziva se kada se pritisne dugme za unos slova i poziva funkciju handleLetterInput) i 
    handleWordInputReference (poziva se kada se pritisne dugme za unos reci i poziva funkciju 
    handleWordInput). Zatim se dodaje dogadjaj klik za sve dugmice na ekranu koji ce pozvati 
    handleLetterClickReference.
   
*/
function setupGame5Listeners(ws) {
    handleLetterClickReference = (event) => handleLetterClick(event, ws);       //kliknuto dugme
    handleLetterInputReference = (event) => handleLetterInput(event, ws);     //submit slovo
    handleWordInputReference = (event) => handleWordInput(event, ws);       //submit rec

    document.querySelectorAll('.keyboard button').forEach(button => {
        button.addEventListener('click', handleLetterClickReference);
    });

    document.querySelector('#submit_letter').addEventListener('click', handleLetterInputReference);
    document.querySelector('#submit_word').addEventListener('click', handleWordInputReference);
}

/*
    uklanja slusaoce dogadjaja koji su prethodno postavljeni u setupGame5Listeners. Funkcija
    radi tako sto se najpre proveri postojanje handleLetterClickReference i ukoliko postoji 
    selektuju se svi dugmici i sa njih se uklanja dogadjaj za klik na dugmice povezan sa 
    handleLetterClickReference. Potom, proverava se postojanje handleLetterInputReference i ako
    postoji uklanja se dogadjaj za pritisak na dugme submit_letter. Potom, proverava se 
    postojanje handleWordInputReference i ako postoji uklanja se dogadjaj za pritisak na dugme submit_word.
*/
function removeGame5Listeners() {
    if (handleLetterClickReference) {
        document.querySelectorAll('.keyboard button').forEach(button => {
            button.removeEventListener('click', handleLetterClickReference);
        });
    }
    if (handleLetterInputReference) {
        document.querySelector('#submit_letter').removeEventListener('click', handleLetterInputReference);
    }
    if (handleWordInputReference) {
        document.querySelector('#submit_word').removeEventListener('click', handleWordInputReference);
    }
}

/*
    poziva se kada korisnik pritisne dugme na ekranu,
    kao ulazne parametre prima event-dogadjaj koji se 
    desio i ws-WebSocket konekcija potrebna kao parametar 
    za handleInput2 funkciju;
    funkcija poziva funkciju handleInput2 sa tekstom dugmeta koje je kliknuto i ws kao argumentima
*/
function handleLetterClick(event, ws) {
    handleInput2(event.target.textContent, ws);
}

/*
    poziva se kada korisnik pritisne dugme na ekranu za unos slova,
    kao ulazne parametre prima event-dogadjaj koji se 
    desio i ws-WebSocket konekcija potrebna kao parametar 
    za handleInput2 funkciju;
    funkcija poziva funkciju handleInput2 sa porukom da je 
    pritisnuto dugme za unos slova
*/
function handleLetterInput(event, ws) {
    handleInput2('EnterLetter', ws);
}

/*
    poziva se kada korisnik pritisne dugme na ekranu za unos reci,
    kao ulazne parametre prima event-dogadjaj koji se 
    desio i ws-WebSocket konekcija potrebna kao parametar 
    za handleInput2 funkciju;
    funkcija poziva funkciju handleInput2 sa porukom da je 
    pritisnuto dugme za unos reci
*/
function handleWordInput(event, ws) {
    handleInput2('EnterWord', ws);
}

/*
    obradjuje unos korisnika (dat kao prvi parametar input), 
    tako sto ukoliko je korisnik uneo slovo, poziva se funkcija za proveru unetog slova checkLetter2 koja prima argument ws,
    ukoliko korisnik uneo rec, poziva se funkcija za proveru unete reci checkWord2 koja prima argument ws,
    i ukoliko je korisnik pritisnuo neko slovo poziva se funkcija za postavljanje tog slova na polje 
    za prikaz pritisnutog slova odnosno addLetter2 koja prima to slovo i ws kao argumente
*/
function handleInput2(input, ws) {
    if (input == 'EnterLetter'){
        checkLetter2(ws);
    } else if (input == 'EnterWord'){
        if (errors==6) game5AnswerSubmitted=true;
        checkWord2(ws);
    }else{
        addLetter2(input,ws);
    }
}

/*
    dodaje slovo na polje namenjeno za prikaz pritisnutog slova,
    kao parametre prima slovo koje unosi i WebSocket 
    konekciju za slanje poruke serveru
*/
function addLetter2(letter, ws) {
    const input_let = document.getElementById(`input_letter`);
    input_let.textContent = letter;
}


/*
    funkcija proverava uneto slovo,
    kao ulazni parametar prima WebSocket konekciju za slanje poruke serveru,
    funkcija salje slovo preko WebSocket-a sa informacijama o unesenom slovu (i neunesenoj reci) 
    i broju nacinjenih gresaka
*/
function checkLetter2(ws) {
    let guessedLetter = '';
    guessedLetter = document.getElementById(`input_letter`).textContent;
    guessedLetter = guessedLetter.toUpperCase();
    console.log("uneto je slovo " + guessedLetter);

    ws.send(JSON.stringify({
        type: 'game5_answer',
        word: null,
        letter: guessedLetter,
        errors: errors
    }));
}

/*
    funkcija proverava unetu rec,
    kao ulazni parametar prima WebSocket konekciju za slanje poruke serveru,
    funkcija salje rec preko WebSocket-a sa informacijama o unesenoj reci (i neunesenom slovu) 
    i broju nacinjenih gresaka
*/
function checkWord2(ws) {
    let guessedWord = "";
    guessedWord = document.getElementById(`input_word`).value;
    if (guessedWord == "") {
        guessedWord = null;
    } else {
        guessedWord = guessedWord.toUpperCase();
    }
    console.log("uneta je rec " + guessedWord);

    ws.send(JSON.stringify({
        type: 'game5_answer',
        word: guessedWord,
        letter: null,
        errors: errors
    }));
}

/*
    postavlja osnovne elemente i logiku potrebnu za rad igre 
    tako sto kreira i postavlja WebSocket konekciju za komunikaciju sa serverom koju cuva u promenljivoj ws,
    postavlja dogadjaje za prvu i drugu igru i ukoliko je treca igra vidljiva na ekranu postavljaju se dogadjaji za trecu igru i inicijalizuje se tabla
*/
function main() {
    // shuffleAnswers();
    // shuffleColumn();
    const ws = setupWebsocketConnection();
    setupTimer(ws);
    setupGame1Listeners(ws);
    setupGame2Listeners(ws);
    
    if (document.getElementById('game3').style.display === 'block') {
        setupGame3Listeners(ws);
        initializeBoard();
    }

    if (document.getElementById('game4').style.display === 'block') {
        // shuffleAnswers();
        //shuffleColumn();
        setupGame4Listeners(ws);
        // initializeCol(); // leftWords, rightWords problem
    }

    // ToDo: setupGame4Listener(ws); + initializeCol();
    if (document.getElementById('game5').style.display === 'block') {
        setupGame5Listeners(ws);
        initializeBoard2();
    }
}

main();
