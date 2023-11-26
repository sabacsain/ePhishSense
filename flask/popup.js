
function clickLogin(){
    document.getElementById('loginCheck').textContent = 'Processing';
    // Get input email and app password
    var emailInput = document.getElementById('input-email').value;
    var passInput = document.getElementById('input-appPassword').value;

    // Send email and password input to the Python Backend
    fetch('http://localhost:5000/api/login', {
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
    // Get the input element by its ID
    var subjectInput = document.getElementById('input-subject').value;

    // Show Processing in GUI
    document.getElementById('buttonCheck').textContent = 'Processing';

    // Send Subject input to the Python Backend
    fetch('http://localhost:5000/api/subject', {
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
    fetch('http://localhost:5000/api/scan')
      .then(response => response.json())
      .then(data => {
        // Display the response
        document.getElementById('buttonCheck').textContent = data.message;
        console.log('Response from Flask:', {'message' : 'Prediction Sent Successfully'});
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
