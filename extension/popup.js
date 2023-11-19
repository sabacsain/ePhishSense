// popup.js

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('scanButton').addEventListener('click', function () {
    chrome.runtime.sendMessage({ action: 'runScan' });
    // document.getElementById('buttonCheck').textContent = 'Button: Working ';
  });

  // Listen for the scan complete message
  chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.action === 'scanComplete') {
      // Display the result in the popup
      // document.getElementById('buttonCheck').textContent = 'Button: Working ';
      // document.getElementById('printCheck').textContent = 'Scan Result: ${message.result}';
      document.getElementById('scanCheck').textContent = `Scan Result: ${message.result}`;
    }
  });
});
