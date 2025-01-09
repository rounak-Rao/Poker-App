


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
