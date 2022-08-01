// var predInterval = null;
// structure is from https://github.com/jimbobbennett/HappySadAngryWorkshop
window.addEventListener("DOMContentLoaded", function() {
    const video = document.getElementById('#video');
    const message = document.getElementById('#msg');
    const button = document.getElementById('#btn');
    const buttonIcon = document.getElementById('#btnicon');
    const scriptBox = document.getElementById('#sbox');
    const sliderOut = document.getElementById('sliderO');

    var pred = false

    var curLetter = " "

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const getImage = async () => {
        video.srcObject = await navigator.mediaDevices.getUserMedia({ video: true })
        video.play();
        }
        getImage()
    }

    button.addEventListener('click', function() {
        if (pred === true) {
        // if (predInterval !== null) {
            // clearInterval(predInterval);
            // predInterval = null;
            // button.textContent = 'Start';

            pred = false

            button.classList.replace('btn-success', 'btn-primary');
            buttonIcon.classList.replace('bi-pause', 'bi-play-circle-fill');
            buttonIcon.style.color = 'darkgreen';
            return;
        }

        var canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        var context = canvas.getContext('2d');
        const FPS = 1;

        function blobToPredict(blob) {
            form = new FormData();
            form.append('image', blob);
            // https://stackoverflow.com/questions/67389537/send-html-video-object-canvas-to-flask-using-ajax
            $.ajax({
                type: "POST",
                url: "/video_pred",
                data: form,
                // timeout: 1000 / FPS,
                processData : false,
                contentType : false, 
                success: function (text) {
                    message.textContent = text;

                    if (pred === true) {
                        let response = text.split('|');
                        let pred_letter = response[0];
                        let prob = parseFloat(response[1]);
                        
                        if (pred_letter === " ") {
                            message.innerHTML = '<span style="font-size: 18pt;color:grey">No hand detected</span>';
                            prob = 1.0
                        }
                        else
                            message.textContent = `Letter ${pred_letter} (prob: ${((prob * 100).toFixed(1))}%)`;

                        let prob_thres = parseFloat(sliderOut.textContent) / 100;
                        if (prob > prob_thres & pred_letter !== curLetter ) {
                            curLetter = pred_letter;
                            scriptBox.textContent += curLetter;
                        }


                        context.drawImage(video, 0, 0, canvas.width, canvas.height);
                        canvas.toBlob(blobToPredict, "image/jpg");
                    }
                    else {
                        message.innerHTML = '<br/>'
                    }
                },
                error: function (data) {
                    // console.warn('There was an error predicting video frames!');
                }
            });
        }

        
        
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        canvas.toBlob(blobToPredict, "image/jpg");
        // clearInterval(predInterval);
        // predInterval = setInterval(() => {
        //     context.drawImage(video, 0, 0, canvas.width, canvas.height);
        //     canvas.toBlob(blobToPredict, "image/jpg");
        // }, 1000/FPS);
        
        pred = true
        // button.textContent = 'Stop';
        button.classList.replace('btn-primary', 'btn-success');
        buttonIcon.classList.replace('bi-play-circle-fill', 'bi-pause');
        buttonIcon.style.color = 'darkgray';

        scriptBox.textContent = '';
        curLetter = " "
        
        // const getResult = async () => {
        //   var result = await fetch('result', {
        //     method: 'POST',
        //     body: JSON.stringify(data),
        //     headers: { 'Content-Type': 'application/json' }
        //   })

        //   var jsonResult = await result.json()
        //   message.textContent = jsonResult.message
        // }
        // getResult()
    });
})