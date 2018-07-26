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
	    ctx.drawImage(elem[0], 0, 0, elem.width(), elem.height());

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

		var data = getBase64Image(video);
		console.log(data);

		showPleaseWait();

		$.ajax({
		    url: 'submit_image',
		    type: 'POST',
		    processData: false,
		    contentType: 'application/base64',
		    data: data
		 })
		.done(function(res) {

			hidePleaseWait();
			console.log(res);

			if (res.error) {

				$('#alert').addClass('alert-danger');
				$('#alert').removeClass('alert-success');
				$('#alert').text('Name not found!');

			} else {

				$('#alert').addClass('alert-success');
				$('#alert').removeClass('alert-danger');
				$('#alert').text('Name found: ' + res.name + '. Message sent!');
			}

			$('#alert').addClass('show');
	    	setTimeout(function() {
		    	$('#alert').removeClass('show');
			}, 5000);
		})
		.fail(function() {

			hidePleaseWait();
			alert("error");
		});
	});

	/**
	 * Displays overlay with "Please wait" text. Based on bootstrap modal. Contains animated progress bar.
	 */
	function showPleaseWait() {
	    var modalLoading = '<div class="modal" id="pleaseWaitDialog" data-backdrop="static" data-keyboard="false" role="dialog">\
	        <div class="modal-dialog">\
	            <div class="modal-content">\
	                <div class="modal-header">\
	                    <h4 class="modal-title">Please wait...</h4>\
	                </div>\
	                <div class="modal-body">\
	                    <div class="progress">\
	                      <div class="progress-bar progress-bar-success progress-bar-striped active" role="progressbar"\
	                      aria-valuenow="100" aria-valuemin="0" aria-valuemax="100" style="width:100%; height: 40px">\
	                      </div>\
	                    </div>\
	                </div>\
	            </div>\
	        </div>\
	    </div>';
	    $(document.body).append(modalLoading);
	    $("#pleaseWaitDialog").modal("show");
	}

	/**
	 * Hides "Please wait" overlay. See function showPleaseWait().
	 */
	function hidePleaseWait() {
	    $("#pleaseWaitDialog").modal("hide");
	}

	// populate the video select
	navigator.mediaDevices.enumerateDevices().then(gotDevices).then(getStream).catch(handleError);
	videoSelect.onchange = getStream;
	
})();
