document.addEventListener('DOMContentLoaded', function () {
  // Add a click event listener to the scan button
  document.getElementById('scanButton').addEventListener('click', function () {
    // When the button is clicked, display "Scan Completed"
    document.getElementById('buttonCheck').textContent = 'Button: Working';
    scanAndDownloadEmlFile();
  });

    // Function to initiate email scan and download
    function scanAndDownloadEmlFile() {
      // Send a message to the content script to trigger the download
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        const activeTabId = tabs[0].id;
        chrome.tabs.sendMessage(activeTabId, { initiateDownload: true });
      });
    }

    // Listen for messages from the content script
    chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
      // Check if the content script has initiated the download
      if (message.downloadInitiated) {
        // Display a message in the popup
        document.getElementById('emlCheck').textContent = 'EML: Downloaded';
      }
  });
});