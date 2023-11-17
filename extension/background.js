// background.js
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === "extractEmailDetails") {
    var emailDetails = request.data;
    detectPhishing(emailDetails);
  } else if (request.action === "scanEmailDetails") {
    // Add logic to initiate the scanning process
    // This could involve accessing Gmail elements and extracting details
    // For simplicity, let's log a message for now
    console.log("Scanning email details initiated");
  }
});

function detectPhishing(emailDetails) {
  console.log("Phishing detection for:", emailDetails);
  // Implement your phishing detection logic here
}

