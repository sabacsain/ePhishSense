// popup.js

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('scanButton').addEventListener('click', function () {
    chrome.runtime.sendMessage({ action: 'runScan' });
  });

  // Listen for the scan complete message
  chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
    if (message.action === 'scanComplete') {
      // Display the result in the popup
      document.getElementById('buttonCheck').textContent = 'Button: Working: ';
      document.getElementById('printCheck').textContent = 'Scan Result: ${message.result}';
      document.getElementById('buttonCheck').textContent = `Scan Result: ${message.result}`;
    }
  });
});
