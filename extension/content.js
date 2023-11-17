// popup.js
document.addEventListener("DOMContentLoaded", function() {
  var scanButton = document.getElementById("scanButton");

  scanButton.addEventListener("click", function() {
    // Communicate with the background script to initiate the scanning process
    chrome.runtime.sendMessage({ action: "scanEmailDetails" });
  });
});

