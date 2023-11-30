var is_authenticated = false;

function checkLogin(){
  // Receive email prediction from the Python Backend
  fetch('http://localhost:5000/api/check_login')
    .then(response => response.json())
    .then(data => {
      console.log(data.message);
      if (data.message == 'Authenticated'){
        is_authenticated = true;
        var emailTextField = document.getElementById("input-email");
        var passTextField = document.getElementById("input-appPassword");
        var loginButton = document.getElementById("loginButton");
        // Disable the input field
        emailTextField.disabled = true;
        passTextField.disabled = true;
        loginButton.disabled = true;
        // Display already authenticated
        document.getElementById('loginCheck').textContent = 'Already logged in';
      }
      // Display the flask response
      console.log('Response from Flask:', data.message);

    })
    .catch(error => {
      console.error('Error:', error);
    });

    return is_authenticated;
}



// Call checkLogin function
checkLogin();




// Get started next html page
document.getElementById("get-started-button").addEventListener("click", function () {
    // Check if the checkbox is checked
    if (is_authenticated) {
        window.location.href = "scan.html";
    } else {
        // If checked, navigate to the next page
        window.location.href = "termsNcondition.html";
    }
    });