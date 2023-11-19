// background.js

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === 'runScan') {
    chrome.runtime.sendNativeMessage('ePhishSense', { command: 'runScan' });
  }
});
