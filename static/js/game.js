document.addEventListener("DOMContentLoaded", () => {
    const seats = document.querySelectorAll(".seat");
    const joinModal = document.getElementById("joinModal");
    const joinBtn = document.getElementById("joinBtn");
    const nameInput = document.getElementById("name");
    const stackInput = document.getElementById("stack");
    const raiseBtn = document.getElementById('raise-btn');
    const raiseSlider = document.getElementById('raise-slider');
    const raiseAmount = document.getElementById('raise-amount');
    const raiseContainer = document.getElementById('raise-container');
    const confirmRaiseBtn = document.getElementById('confirm-raise');
    let selectedSeat = null;

    // Start/End Game Button
    const gameButton = document.getElementById('start-end-game-btn');

    // Connect to Socket.io
    var socket = io();

    socket.emit('message', 'Hello from the game page!');

    socket.on('update', function (data) {
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

    socket.on('seat_updated', function (data) {
        const seat = document.querySelector(`[data-seat="${data.seat_index}"]`);
        seat.textContent = `${data.name} - $${data.stack}`;
        seat.setAttribute('data-player', data.name);
        seat.style.backgroundColor = "#5cb85c";
        seat.classList.add('occupied');
        joinModal.style.display = "none";
    });

    // Handle error messages from the backend
    socket.on('error', function (data) {
        alert(data.message);
    });

    window.addEventListener("click", (e) => {
        if (e.target === joinModal) {
            joinModal.style.display = "none";
        }
    });

    // When the Start/End Game button is clicked, toggle the game state
    gameButton.addEventListener('click', () => {
        console.log('btn clicked')
        socket.emit('toggle_game'); // Emit event to toggle the game
    });

    // Listen for updates to the button text (Start/End)
    socket.on('update_button', function (data) {
        console.log("Received update_button:", data);
        gameButton.textContent = data.button_text;  // Update the button text
    });

    // Handle game start event (disable button or show message)
    socket.on('game_started', function () {
        console.log("Game Started");
        gameButton.disabled = false; // Disable the button after game starts
    });

    // Handle game end event (re-enable button)
    socket.on('game_ended', function () {
        console.log("Game Ended");
        gameButton.disabled = false; // Re-enable the button for a new game
    });

    socket.on('cards_dealt', function (data) {
        console.log('Received cards:', data);

        Object.entries(data).forEach(([seatIndex, cards]) => {
            const playerSeat = document.querySelector(`.seat[data-seat="${seatIndex}"]`);
            if (playerSeat) {
                // Check if a card-container already exists
                let cardContainer = playerSeat.querySelector('.card-container');
                if (!cardContainer) {
                    // Create a new card-container dynamically
                    cardContainer = document.createElement('div');
                    cardContainer.classList.add('card-container');
                    playerSeat.appendChild(cardContainer);
                }

                // Clear existing cards in the card-container
                cardContainer.innerHTML = '';

                // Add cards to the card-container
                cards.forEach(card => {
                    const img = document.createElement('img');
                    img.src = `/static/cards/classic/${card}.png`; // Path to your card images
                    img.alt = card;
                    img.classList.add('card-image'); // Apply the .card-image class for styling
                    cardContainer.appendChild(img);
                });
            } else {
                console.error(`No seat found for seat index: ${seatIndex}`);
            }
        });
    });

    const setBlindsButton = document.getElementById('set-blinds-btn');

    setBlindsButton.addEventListener('click', () => {
        const smallBlind = parseFloat(document.getElementById('small-blind').value);
        const bigBlind = parseFloat(document.getElementById('big-blind').value);

        if (smallBlind >= 0 && bigBlind > smallBlind) {
            socket.emit('set_blinds', { small: smallBlind, big: bigBlind });
            document.getElementById('blind-display').textContent = `Blinds: ${smallBlind}/${bigBlind}`;
        } else {
            alert('Invalid blind values. Ensure BB > SB and both are positive.');
        }
    });

    raiseBtn.addEventListener('click', toggleRaise);
    raiseSlider.addEventListener('input', function() {
        updateRaiseAmount(raiseSlider.value);
    });
    raiseAmount.addEventListener('change', function() {
        updateSliderValue(raiseAmount.value);
    });
    confirmRaiseBtn.addEventListener('click', function() {
        const raiseValue = parseInt(raiseAmount.value);
        // Example emit to backend
        socket.emit('raise', { raiseAmount: raiseValue });
    });
});

// Show or hide raise container
function toggleRaise() {
    const raiseContainer = document.getElementById('raise-container');
    raiseContainer.style.display = raiseContainer.style.display === 'none' ? 'flex' : 'none';
}

// Update the raise amount in the number input
function updateRaiseAmount(value) {
    document.getElementById('raise-amount').value = value;
}

// Update the slider value from the number input
function updateSliderValue(value) {
    const slider = document.getElementById('raise-slider');
    if (value < slider.min) value = slider.min;
    if (value > slider.max) value = slider.max;
    slider.value = value;
}

socket.on('game_state', function(data) {
    const { current_seat, current_bet, player_stack } = data;

    // Highlight the player's seat whose turn it is
    const allSeats = document.querySelectorAll(".seat");
    allSeats.forEach(seat => {
        seat.style.border = '';  // Remove highlight from all seats
        seat.classList.remove('current-turn');
    });

    const currentSeat = document.querySelector(`[data-seat="${current_seat}"]`);
    if (currentSeat) {
        currentSeat.style.border = '2px solid red';  // Highlight the player's seat
        currentSeat.classList.add('current-turn');
    }

    // Update the player's stack
    const stackDisplay = currentSeat.querySelector('.stack');
    if (stackDisplay) {
        stackDisplay.textContent = `$${player_stack}`;
    }

    // Update the raise slider and amount
    updateSliderValue(current_bet);
});

