
function result(){
  // Receive email prediction from the Python Backend
  fetch('http://localhost:5000/api/get_result')
    .then(response => response.json())
    .then(data => {
        // Display already authenticated
      document.getElementById('get-result').textContent = data.message;
      // Display the flask response
      console.log('Response from Flask:', data.message);
    })
    .catch(error => {
      console.error('Error:', error);
    });

    return;
}



// Call getResult function
result();

