var is_authenticated = false;

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
      if (data.message == 'Login SUCCESSFUL'){
        is_authenticated = true;
        window.location.href = "scan.html";
      } else {
        is_authenticated = false;
        alert("LOGIN FAILED");
      }
  })
  .catch(error => {
      console.error('Error sending data to Flask:', error);
  });

  // Clear Password
    var emailInput = ''
    var passInput = ''

    return is_authenticated
}




document.addEventListener('DOMContentLoaded', function () {

// Call clickLogin function
document.getElementById('loginButton').addEventListener('click', clickLogin);

});

