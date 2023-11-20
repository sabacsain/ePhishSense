document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('scanButton').addEventListener('click', function () {
    // Make a request to the Python backend
    fetch('http://localhost:5000/api/ephishsense')
      .then(response => response.json())
      .then(data => {
        alert(data.message);  // Display the response
      })
      .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Check the console for details.');
      });
  });
});
