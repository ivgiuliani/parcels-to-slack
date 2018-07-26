(function () {
    'use strict';

    // globals
	const video = document.getElementById('video');

    function getBase64Image(img) {
	    // Create an empty canvas element
	    var canvas = document.createElement('canvas');

	    // TODO: get rid of the video selector
	    canvas.width = $('#video').width();
	    canvas.height = $('#video').height();
	    console.log(canvas);

	    // Copy the image contents to the canvas
	    var ctx = canvas.getContext('2d');
	    ctx.drawImage(img, 0, 0);

	    // Get the data-URL formatted image
	    // Firefox supports PNG and JPEG. You could check img.src to
	    // guess the original format, but be aware the using "image/jpg"
	    // will re-encode the image.
	    var dataURL = canvas.toDataURL('image/png');

	    return dataURL.replace(/^data:image\/(png|jpg);base64,/, '');
	}

	navigator.mediaDevices.enumerateDevices()
	  .then(gotDevices).then(getStream).catch(handleError);

	videoSelect.onchange = getStream;

	function gotDevices(deviceInfos) {
	  for (let i = 0; i !== deviceInfos.length; ++i) {
	    const deviceInfo = deviceInfos[i];
	    const option = document.createElement('option');
	    option.value = deviceInfo.deviceId;
	    if (deviceInfo.kind === 'videoinput') {
	      option.text = deviceInfo.label || 'camera ' +
	        (videoSelect.length + 1);
	      videoSelect.appendChild(option);
	    } else {
	      console.log('Found another kind of device: ', deviceInfo);
	    }
	  }
	}

	function getStream() {
	  if (window.stream) {
	    window.stream.getTracks().forEach(function(track) {
	      track.stop();
	    });
	  }

	  const constraints = {
	    video: {
	      deviceId: {exact: videoSelect.value}
	    }
	  };

	  navigator.mediaDevices.getUserMedia(constraints).
	    then(gotStream).catch(handleError);
	}

	function gotStream(stream) {
	  window.stream = stream; // make stream available to console
	  video.srcObject = stream;
	}

	function handleError(error) {
	  console.error('Error: ', error);
	}

	// Trigger photo take
	document.getElementById('snap').addEventListener('click', function() {
		console.log(getBase64Image(video));
		// video.pause();
	});
})();
