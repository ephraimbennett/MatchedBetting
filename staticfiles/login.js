document.addEventListener('DOMContentLoaded', (event) => {
    var token = document.querySelector("[name=csrfmiddlewaretoken]");
    console.log(token);

    document.querySelector('form').onsubmit = function() {
        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;
        
        if (email.trim() === '' || password.trim() === '') {
            alert('Please fill in all fields.');
            return false; // Prevent form submission
        }
        return true; // Allow form submission
    };
    
});
