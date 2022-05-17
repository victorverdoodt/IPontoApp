var LOADING = false;

// Grab elements, create settings, etc.
var video = document.getElementById('video');

// Get access to the camera!
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        //video.src = window.URL.createObjectURL(stream);
        video.srcObject = stream;
        video.play();
    });
}

// Elements for taking the snapshot
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var video = document.getElementById('video');

// Trigger photo take
document.getElementById("snap").addEventListener("click", function() {
    if (document.getElementById('name').value.length < 1) {
      alert('Must provide a name!');
      return
    }
    if (LOADING) {
      console.log('wait for image')
      return
    }
    context.drawImage(video, 0, 0, 640, 480);
    convertCanvasToImage(canvas, (image) => upload(image))
});

// Converts canvas to an image
function convertCanvasToImage(canvas, upload) {
  let image = new Image();
  image = canvas.toDataURL("image/png");
  // displays image
  // document.getElementById('results').innerHTML = '<img id="image" src="'+image+'"/>';
  upload(image);
}

function upload(image) {
    LOADING = true;
    console.log("Uploading...");
    document.getElementById('message').innerHTML = "Uploading...";
    var name = document.getElementById('name').value;
    var compare = document.getElementById('compare').checked;

    // build the form
    var formData = new FormData();
    formData.append("file", image);
    formData.append("name", name);
    formData.append("compare", compare);
    var xmlhttp = new XMLHttpRequest();
    // choose right endpoint
    var url = compare !== true ? "/upload" : "compare";
    xmlhttp.open("POST", url);

    // check when state changes,
    xmlhttp.onreadystatechange = function() {
        if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
          var logger = document.getElementById('message');
          logger.innerHTML = null;
          LOADING = false;
            document.getElementById('content').innerHTML = xmlhttp.response;

        }
    };

    xmlhttp.send(formData);
}