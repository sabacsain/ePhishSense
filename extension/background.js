// background.js

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === 'runScan') {
    chrome.runtime.sendNativeMessage('your_native_app_name', { command: 'runScan' }, function (response) {
      // Send a message to the popup with the result
      chrome.runtime.sendMessage({ action: 'scanComplete', result: response.result });
    });
  }
});
