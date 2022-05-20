var LOADING = false;

// Grab elements, create settings, etc.
var video = document.getElementById('video');
var haveVideo = false;
// Get access to the camera!
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        //video.src = window.URL.createObjectURL(stream);
        video.srcObject = stream;
        video.play();
        haveVideo = true;
    }).catch(function(err) {
            console.log("Unable to capture WebCam.", err);
             haveVideo = false;
    });
}

// Elements for taking the snapshot
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var video = document.getElementById('video');

// Trigger photo take
document.getElementById("snap").addEventListener("click", function() {
    if(!haveVideo){
        alert('Precisa de camera')
        return
    }
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
    document.getElementById('message').innerHTML = "Enviando...";
    var name = document.getElementById('name').value;

    // build the form
    var formData = new FormData();
    formData.append("file", image);
    formData.append("name", name);
    var xmlhttp = new XMLHttpRequest();
    // choose right endpoint
    var url =  "/upload";
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