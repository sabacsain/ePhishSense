function clickScan(){
  console.log('SCAN START')
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
      console.log('Response from Flask:', {'message' : 'Scan result has been SENT'});
    })
    .catch(error => {
      console.error('Error:', error);
    });
  console.log('SCAN END')
}


document.addEventListener('DOMContentLoaded', function () {

  // Call clickScan function
document.getElementById('scanButton').addEventListener('click', clickScan);


});
