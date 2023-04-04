// Get all elements with class="closebtn"
(function(){
    var form = document.getElementById('file-form');
    var fileSelect = document.getElementById('filename');
    var uploadButton = document.getElementById('submit');
    var statusDiv = document.getElementById('status');

    form.onsubmit = function(event) {
        event.preventDefault();

        statusDiv.innerHTML = 'Uploading . . . ';

        // Get the files from the input
        var files = fileSelect.files;

        // Create a FormData object.
        var formData = new FormData();

        //Grab only one file since this script disallows multiple file uploads.
        var file = files[0]; 

         // Add the file to the AJAX request.
        formData.append('filename', file, file.name);

        // Set up the request.
        var xhr = new XMLHttpRequest();

        // Open the connection.
        xhr.open('POST', '/muebles', true);
    

        // Set up a handler for when the task for the request is complete.
        xhr.onload = function () {
          if (xhr.status === 200) {
            statusDiv.innerHTML = 'Your upload is successful..';
          } else {
            statusDiv.innerHTML = 'An error occurred during the upload. Try again.';
          }
        };

        // Send the data.
        xhr.send(formData);
    }
})();