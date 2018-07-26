(function () {
    'use strict';

    // globals
	const video = $('video');

    function getBase64Image(elem) {
	    // create an empty canvas element
	    var canvas = document.createElement('canvas');

	    canvas.width = elem.width();
	    canvas.height = elem.height();

	    // copy the image contents to the canvas
	    var ctx = canvas.getContext('2d');
	    ctx.drawImage(elem[0], 0, 0);

	    // Get the data-URL formatted image
	    // Firefox supports PNG and JPEG. You could check img.src to
	    // guess the original format, but be aware the using "image/jpg"
	    // will re-encode the image.
	    var dataURL = canvas.toDataURL('image/png');

	    return dataURL.replace(/^data:image\/(png|jpg);base64,/, '');
	}

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
	      // console.log('Found another kind of device: ', deviceInfo);
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
	  video[0].srcObject = stream;
	}

	function handleError(error) {
	  console.error('Error: ', error);
	}

	// Trigger photo take
	video.click(function(e){

	    console.log(getBase64Image(video));
	    alert('got it');
	    // video[0].pause();
	});

	// populate the video select
	navigator.mediaDevices.enumerateDevices().then(gotDevices).then(getStream).catch(handleError);
	videoSelect.onchange = getStream;
	
})();
