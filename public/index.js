var video = document.querySelector("#videoElement");

if (navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then(function (stream) {
      video.srcObject = stream;
      webcamStream = stream;
      // send the stream to the server from client
    })
    .catch(function (err0r) {
      console.log("Something went wrong!");
    });
}
