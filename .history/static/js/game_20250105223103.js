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


// Wait for the document to be ready
document.addEventListener("DOMContentLoaded", function () {
    const startButton = document.getElementById('startGameButton');

    // Listen for the start button click
    startButton.addEventListener('click', function() {
        // Emit event to backend (via socket.io or an AJAX call)
        socket.emit('start_game');

        // Change the button text to "End Game"
        startButton.innerText = 'End Game';

        // Optionally, disable the button after it's clicked
        startButton.disabled = true;
    });
});
