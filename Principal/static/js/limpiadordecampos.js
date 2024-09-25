document.addEventListener("DOMContentLoaded", function() {
    // Select all error messages
    var errorMessages = document.querySelectorAll('.errorlist');
    
    // Set a timeout to hide them after 5 seconds (5000 milliseconds)
    setTimeout(function() {
        errorMessages.forEach(function(error) {
            error.style.display = 'none';
        });
    }, 2000); // Change the time in milliseconds as needed
});