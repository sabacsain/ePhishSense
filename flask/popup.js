document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('scanButton').addEventListener('click', function () {
    // Get the input element by its ID
    var subjectInput = document.getElementById('myInput').value;

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

    // Receive email result from the Python Backend
    fetch('http://localhost:5000/api/ephishsense')
      .then(response => response.json())
      .then(data => {
        // Display the response
        document.getElementById('buttonCheck').textContent = data.message;
        console.log('Response from Flask:', 'Data Received!');
      })
      .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Check the console for details.');
      });
  });
});
