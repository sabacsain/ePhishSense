
document.addEventListener('DOMContentLoaded', function () {
  // Error handling for checkbox
  document.getElementById("nextButton").addEventListener("click", function () {
    // Check if the checkbox is checked
    if (!document.getElementById("acceptTermsCheckbox").checked) {
        alert("Please accept the Terms and Conditions before proceeding.");
    } else {
        // If checked, and not authenticated navigate to the login page
        window.location.href = "login.html";
    }
    });
});



