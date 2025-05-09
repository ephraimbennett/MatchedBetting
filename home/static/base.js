

function logout() {
    csrftoken = getCookie('csrftoken');
    fetch('/logout/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({info : 'logout'})
    })
    .then(response => response.json())
    .then(data => {
        // Handle success
        console.log(data.message)
        if (data.message == "Successful Logout") {
            window.href = "/";
            location.reload(true);
        }
    })
    .catch(error => {
        // Handle error
        console.log("ERR: " + error)
    });
    
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
