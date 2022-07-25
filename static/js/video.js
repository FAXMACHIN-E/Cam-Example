var predInterval = null;
window.addEventListener("DOMContentLoaded", function() {
    var video = document.getElementById('#video');
    var message = document.getElementById('#msg');
    var button = document.getElementById('#btn');
    var buttonIcon = document.getElementById('#btnicon');

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        const getImage = async () => {
        video.srcObject = await navigator.mediaDevices.getUserMedia({ video: true })
        video.play();
        }
        getImage()
    }

    button.addEventListener('click', function() {
        if (predInterval !== null) {
        clearInterval(predInterval);
        predInterval = null;
        // button.textContent = 'Start';
        button.classList.replace('btn-success', 'btn-primary');
        buttonIcon.classList.replace('bi-pause', 'bi-play');
        return;
        }

        var canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const FPS = 1;

        function blobToPredict(blob) {
            form = new FormData();
            form.append('image', blob);
            // https://stackoverflow.com/questions/67389537/send-html-video-object-canvas-to-flask-using-ajax
            $.ajax({
                type: "POST",
                url: "/video_pred",
                data: form,
                timeout: 1000 / FPS,
                processData : false,
                contentType : false, 
                success: function (text) {
                    message.textContent = text
                },
                error: function (data) {
                    console.warn('There was an error predicting video frames!');
                }
            }).done(function (text) {
                // message.textContent = text;
                console.log("Capture sent");
            }).fail(function(jqXHR, textStatus){
                if(textStatus === 'timeout')
                {     
                    console.warn('Failed from timeout'); 
                    //do something. Try again perhaps?
                }
            });
        }

        
        var context = canvas.getContext('2d');
        clearInterval(predInterval);
        predInterval = setInterval(() => {
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            canvas.toBlob(blobToPredict, "image/jpg");
        }, 1000/FPS);
        
        // button.textContent = 'Stop';
        button.classList.replace('btn-primary', 'btn-success');
        buttonIcon.classList.replace('bi-play', 'bi-pause');
        
        
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