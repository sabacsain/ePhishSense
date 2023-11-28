


function clickLogin(){
  const proxyUrl = 'https://api.allorigins.win/raw?url=';
  const apiLogin = 'https://ephishsense.onrender.com/api/login';
  const localLogin = 'http://127.0.0.1:5000/api/login'

    document.getElementById('loginCheck').textContent = 'Processing';
    // Get input email and app password
    var emailInput = document.getElementById('input-email').value;
    var passInput = document.getElementById('input-appPassword').value;

    // Send email and password input to the Python Backend
    fetch(apiLogin, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: emailInput, password: passInput }),
    })
    .then()
    .then(response => response.json())
    .then(data => {
        console.log('Response from Flask:', data);
        // Show login successful in GUI
        document.getElementById('loginCheck').textContent = data.message;
    })
    .catch(error => {
        console.error('Error sending data to Flask:', error);
    });

    // Clear Password
      var emailInput = 'None'
      var passInput = 'None'
}

function clickScan(){
  const proxyUrl = 'https://api.allorigins.win/raw?url=';
  const apiSubject = 'https://ephishsense.onrender.com/api/subject';
  const apiScan = 'https://ephishsense.onrender.com/api/scan';
  const localSubject = 'http://127.0.0.1:5000/api/subject'
  const localScan = 'http://127.0.0.1:5000/api/scan'

    // Get the input element by its ID
    var subjectInput = document.getElementById('input-subject').value;

    // Show Processing in GUI
    document.getElementById('buttonCheck').textContent = 'Processing';

    // Send Subject input to the Python Backend
    fetch(apiSubject, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({data: subjectInput}),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from Flask:', data);
    })
    .catch(error => {
        console.error('Error sending data to Flask:', error);
    });

    // Receive email prediction from the Python Backend
    fetch(apiScan)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        // Display the response
        document.getElementById('buttonCheck').textContent = data.message;
        console.log('Response from Flask:', {'message' : 'Scan result has been SENT'});
      })
      .catch(error => {
        console.error('Error:', error);
      });
}

document.addEventListener('DOMContentLoaded', function () {

  // Call clickLogin function
  document.getElementById('loginButton').addEventListener('click', clickLogin);

  // Call clickScan function
  document.getElementById('scanButton').addEventListener('click', clickScan);

  
});
