// popup.js

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('connectButton').addEventListener('click', function () {
    // Open the Flask application in a new tab
    chrome.tabs.create({ 'url': 'http://localhost:5000' });
  });
});
