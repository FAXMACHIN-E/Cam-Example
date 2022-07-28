window.addEventListener("DOMContentLoaded", function() {
  const videoElement = document.getElementById('#video');
  const message = document.getElementById('#msg');
  const button = document.getElementById('#btn');
  const buttonIcon = document.getElementById('#btnicon');

  var pred = false

  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const getImage = async () => {
        videoElement.srcObject = await navigator.mediaDevices.getUserMedia({ video: true })
        videoElement.play();
      }
      getImage()
  }


  // videoElement.style.display = "none";
  // const canvasElement = document.getElementsByClassName('output_canvas')[0];
  // canvasElement.style.display = "none"
  // const canvasCtx = canvasElement.getContext('2d');
  
  // function onResults(results) {
  //   canvasCtx.save();
  //   canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  //   canvasCtx.drawImage(
  //       results.image, 0, 0, canvasElement.width, canvasElement.height);
  //   if (results.multiHandLandmarks) {
  //     for (const landmarks of results.multiHandLandmarks) {
  //       drawConnectors(canvasCtx, landmarks, HAND_CONNECTIONS,
  //                      {color: '#00FF00', lineWidth: 2});
  //       drawLandmarks(canvasCtx, landmarks, {color: '#FF0000', lineWidth: 0.01, radius: 4} );
  //     }
  //   }
  //   canvasCtx.restore();
  // }    

  async function sleep(ms) {
    return new Promise(r => setTimeout(r, ms))
  }

  var canvas = document.createElement('canvas');
  canvas.width = videoElement.videoWidth;
  canvas.height = videoElement.videoHeight;
  var context = canvas.getContext('2d');

  async function canvasToImage(canvas) {
    let image = await new Image();
    image.src = await canvas.toDataURL("image/jpeg");
    return image;
  }

  async function onRes(results) {
    if (results.multiHandLandmarks.length === 0) {
      message.innerHTML = '<span style="font-size: 18pt;color:grey">No hand detected</span>'
      await sleep(200)
    } else {
      const text = await $.ajax({
        url: '/mediapipe_pred',
        type: 'POST',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({
          'multiHandLandmarks': results.multiHandLandmarks,
          'multiHandWorldLandmarks': results.multiHandWorldLandmarks,
        })
      });
      message.textContent = text;
      
    }
    if (pred === true) {
      await sleep(100)        
      hands.send({image: videoElement});
    }  
    else {
      message.innerHTML = '<br/>'
    }
  }

  const hands = new Hands({locateFile: (file) => {
    return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
  }});
  hands.setOptions({
    maxNumHands: 2,
    modelComplexity: 1,
    minDetectionConfidence: 0.3,
    minTrackingConfidence: 0.3
  });
  hands.onResults(onRes);
  
  async function onBtnClick() {
    if (pred === false) {
      pred = true;
      // button.classList.replace('btn-primary', 'btn-success');
      buttonIcon.classList.replace('bi-play-circle-fill', 'bi-pause');
      buttonIcon.style.color = 'grey';
      message.innerHTML = `
      <div class="d-flex align-items-center" style="font-size: 18pt;color:grey">
        Loading Mediapipe to your browser... &nbsp;&nbsp;&nbsp;&nbsp;
        <div class="spinner-border" role="status" aria-hidden="true"></div>
      </div>
      `;
      await hands.send({image: videoElement})
    }
    else {
      pred = false;
      // button.classList.replace('btn-success', 'btn-primary');
      buttonIcon.classList.replace('bi-pause', 'bi-play-circle-fill');
      buttonIcon.style.color = 'darkgreen';
    }
    
  }
  
  button.addEventListener('click', () => onBtnClick())
});