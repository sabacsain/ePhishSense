// background.js

// Function to check if the sender's email address exists
function checkSenderEmailExistence(senderEmailAddress) {
  // Replace this with your logic to check if the email address exists
  // For demonstration purposes, it always returns true
  return true;
}

// Listen for messages from content script
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.checkSender) {
    // Check if the sender's email address exists
    const isSenderExisting = checkSenderEmailExistence(message.senderEmailAddress);

    // Broadcast the result to all extension components
    chrome.runtime.sendMessage({ senderExists: isSenderExisting });
  }
});
