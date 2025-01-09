var socket = io();

socket.emit('message', 'Hello from the game page!');
socket.on('update', function(data) {
    console.log('Game state updated:', data);
});

document.addEventListener("DOMContentLoaded", () => {
    const seats = document.querySelectorAll(".seat");
    const joinModal = document.getElementById("joinModal");
    const joinBtn = document.getElementById("joinBtn");
    const nameInput = document.getElementById("name");
    const stackInput = document.getElementById("stack");
    let selectedSeat = null;

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
});


document.addEventListener('DOMContentLoaded', function () {
    const gameButton = document.getElementById('start-end-game-btn');

    // Connect to Socket.io
    const socket = io();

    // When the button is clicked, toggle the game state
    gameButton.addEventListener('click', function() {
        socket.emit('toggle_game');
    });

    // Update the button text when the game starts
    socket.on('update_button', function(data) {
        gameButton.textContent = data.button_text;  // Update button text (Start/End)
    });

    // Handle game start (e.g., to disable the button once the game starts)
    socket.on('game_started', function() {
        console.log("Game Started");
        // Optionally, disable the button after starting the game:
        gameButton.disabled = true;
    });

    // Handle game end
    socket.on('game_ended', function() {
        console.log("Game Ended");
        // Optionally, enable the button to start a new game:
        gameButton.disabled = false;
    });
});
