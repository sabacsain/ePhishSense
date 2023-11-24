// background.js
let mail = '';

chrome.runtime.onInstalled.addListener(function () {
  // Initialize or load data when the extension is installed or updated
  // Example: storedData = loadStoredData();
});

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === 'storeData') {
    // Store data
    mail = request.data;
    console.log('BGJS Receive mail POPUP');
    console.log(mail);
    // Optionally, save the data to persistent storage (e.g., chrome.storage.sync)
    // saveDataToStorage(storedData);
    // Send a response if needed
    sendResponse({ message: 'Data stored successfully' });
  } else if (request.action === 'getData') {
    // Retrieve data
    // You can use storedData for your logic or fetch it from persistent storage
    // storedData = loadDataFromStorage();
    // Send the data back to the sender (e.g., the popup script)
    sendResponse({ data: mail });
    console.log('BGJS Send mail to POPJS');
    console.log(mail);
  }
});