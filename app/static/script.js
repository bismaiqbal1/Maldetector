document.addEventListener('DOMContentLoaded', function() {
  // Get the form element
  var form = document.getElementById('form');

  // Add event listener to the form submission
  form.addEventListener('submit', function(event) {
    // Get the file input element
    var fileInput = document.querySelector('input[type="file"]');
    // Get the selected file
    var file = fileInput.files[0];

    // Check if a file is selected
    if (!file) {
      alert('Please select a file to upload.');
      event.preventDefault(); // Prevent form submission
      return;
    }

    // Get the file extension
    var fileExtension = file.name.split('.').pop().toLowerCase();

    // Check if the file extension is not apk
    if (fileExtension !== 'apk') {
      alert('Please upload a .apk file.');
      event.preventDefault(); // Prevent form submission
      return;
    }
  });
});
