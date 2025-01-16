document.addEventListener("DOMContentLoaded", () => {
    const seats = document.querySelectorAll(".seat");
    const joinModal = document.getElementById("joinModal");
    const joinBtn = document.getElementById("joinBtn");
    const nameInput = document.getElementById("name");
    const stackInput = document.getElementById("stack");
    let selectedSeat = null;

    // Start/End Game Button
    const gameButton = document.getElementById('start-end-game-btn');
    
    // Connect to Socket.io
    var socket = io();

    socket.emit('message', 'Hello from the game page!');

    socket.on('update', function(data) {
        console.log('Game state updated:', data);
    });

    // Handle joining a seat
    seats.forEach(seat => {
        seat.addEventListener("click", () => {
            if (!seat.classList.contains('occupied')) {
                selectedSeat = seat;
                joinModal.style.display = "flex";
            }
        });
    });

    joinBtn.addEventListener("click", () => {
        const name = nameInput.value;
        const stack = stackInput.value;

        if (name && stack) {
            /*
            selectedSeat.textContent = `${name} - $${stack}`;
            selectedSeat.style.backgroundColor = "#5cb85c";
            selectedSeat.classList.add('occupied')
            joinModal.style.display = "none";
            */
            socket.emit('join_seat', {
                seat_index: selectedSeat.dataset.seat,
                name: name,
                stack: stack
            });

            nameInput.value = "";
            stackInput.value = "";
        } else {
            alert("Please enter both name and stack.");
        }
    });

    socket.on('seat_updated', function(data) {
        const seat = document.querySelector(`[data-seat="${data.seat_index}"]`);
        seat.textContent = `${data.name} - $${data.stack}`;
        seat.setAttribute('data-player', data.name);
        seat.style.backgroundColor = "#5cb85c";
        seat.classList.add('occupied');
        joinModal.style.display = "none";
    });
    
    // Handle error messages from the backend
    socket.on('error', function(data) {
        alert(data.message);
    });

    window.addEventListener("click", (e) => {
        if (e.target === joinModal) {
            joinModal.style.display = "none";
        }
    });

    // When the Start/End Game button is clicked, toggle the game state
    gameButton.addEventListener('click', ()=> {
        console.log('btn clicked')
        socket.emit('toggle_game'); // Emit event to toggle the game
    });

    // Listen for updates to the button text (Start/End)
    socket.on('update_button', function(data) {
        console.log("Received update_button:", data);
        gameButton.textContent = data.button_text;  // Update the button text
    });

    // Handle game start event (disable button or show message)
    socket.on('game_started', function() {
        console.log("Game Started");
        gameButton.disabled = true; // Disable the button after game starts
    });

    // Handle game end event (re-enable button)
    socket.on('game_ended', function() {
        console.log("Game Ended");
        gameButton.disabled = false; // Re-enable the button for a new game
    });

/
    socket.on('cards_dealt', function(data) {
        console.log('Received cards:', data);
        Object.entries(data).forEach(([seatIndex, cards]) => {
            const playerSeat = document.querySelector(`.seat[data-seat="${seatIndex}"]`);
            if (playerSeat) {
                // Clear any existing cards (in case cards were dealt previously)
                playerSeat.innerHTML = `Seat ${seatIndex}`; // Reset seat text
                
                cards.forEach(card => {
                    const img = document.createElement('img');
                    img.src = `/static/cards/classic/${card}.png`; // Path to your card images
                    img.alt = card;
                    img.classList.add('card-image'); // Add CSS class for styling
                    playerSeat.appendChild(img); // Append card image directly to seat
                });
            } else {
                console.error(`No seat found for seat index: ${seatIndex}`);
            }
        });
    });
    
 
/*
    socket.on('cards_dealt', function(data) {
        console.log('Received cards:', data);
        Object.entries(data).forEach(([seatIndex, cards]) => {
            const playerSeat = document.querySelector(`.seat[data-seat="${seatIndex}"]`);
            if (playerSeat) {
                console.log(`Found seat for index ${seatIndex}:`, playerSeat);
                const cardContainer = playerSeat.querySelector('.card-container');
                console.log('found card container: ', cardContainer);
                if (cardContainer) {
                    cardContainer.innerHTML = ''; // Clear existing cards
                    
                    cards.forEach(card => {
                        const img = document.createElement('img');
                        img.src = `/static/cards/classic/${card}`; // Path to your card images
                        img.alt = card;
                        img.classList.add('card-image'); // Add CSS class for styling
                        cardContainer.appendChild(img);
                    });
                } else {
                    console.error(`Card container not found for seat ${seatIndex}`);
                }
            } else {
                console.error(`No seat found for seat index: ${seatIndex}`);
            }
        });
    });
*/
});
