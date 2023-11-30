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
      console.log('Response from Flask:', {'message' : 'Scan result has been SENT'});
      if (data.message == 'Safe'){
        window.location.href = "safe.html";
      }
      else if(data.message == 'Malicious'){
        window.location.href = "malicious.html";
      }
      // document.getElementById('buttonCheck').textContent = data.message;
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