// background.js

// Listen for messages from popup.js
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.message === 'startOAuthFlow') {
    // Start the OAuth flow
    chrome.identity.getAuthToken({ interactive: true }, function (token) {
      if (chrome.runtime.lastError) {
        // Handle errors
        console.error(chrome.runtime.lastError);
        sendResponse({ status: 'Failed to connect to Gmail API.' });
      } else {
        // Token obtained successfully, display success message
        console.log('Token obtained:', token);
        sendResponse({ status: 'Connected to Gmail API!' });
      }
    });

    // Return true to indicate that we want to use sendResponse asynchronously
    return true;
  }
});
