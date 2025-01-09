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

