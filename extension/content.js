// content.js

// Function to extract the sender's email address from a Gmail email element
function extractSenderEmailAddress(emailElement) {
  const senderElement = emailElement.querySelector('[email]');
  return senderElement ? senderElement.getAttribute('email') : null;
}

// Function to trigger the download of the email as .eml file
function downloadEmlFile(emailElement) {
  const emailBody = emailElement.querySelector('[role="listitem"]').outerHTML;
  const senderEmailAddress = extractSenderEmailAddress(emailElement);

  const blob = new Blob([emailBody], { type: 'message/rfc822' });
  const blobUrl = URL.createObjectURL(blob);

  const filename = `${senderEmailAddress}_email.eml`;

  // Trigger the download
  chrome.downloads.download({
    url: blobUrl,
    filename: filename,
    saveAs: true,
  });

  // Inform the popup that the download has been initiated
  chrome.runtime.sendMessage({ downloadInitiated: true });
}

// Listen for messages from the popup
chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  // Check if the popup has initiated the download
  if (message.initiateDownload) {
    // Find the email element on the page and trigger the download
    const emailElement = document.querySelector('[role="listitem"][tabindex="0"]');
    if (emailElement) {
      downloadEmlFile(emailElement);
    }
  }
});
