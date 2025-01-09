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
    const socket = io();

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
            selectedSeat.textContent = `${name} - $${stack}`;
            selectedSeat.style.backgroundColor = "#5cb85c";
            selectedSeat.classList.add('occupied')
            joinModal.style.display = "none";

            socket.emit('join_seat', {
                seat: selectedSeat.dataset.seat,
                name: name,
                stack: stack
            });

            nameInput.value = "";
            stackInput.value = "";
        } else {
            alert("Please enter both name and stack.");
        }
    });

    window.addEventListener("click", (e) => {
        if (e.target === joinModal) {
            joinModal.style.display = "none";
        }
    });

    // When the Start/End Game button is clicked, toggle the game state
    gameButton.addEventListener('click', () {
        socket.emit('toggle_game'); // Emit event to toggle the game
    });

    // Listen for updates to the button text (Start/End)
    socket.on('update_button', function(data) {
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
});
