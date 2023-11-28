document.getElementById('snap').addEventListener('click', function() {
    // 获取视频流
    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        .then(function(stream) {
            const video = document.getElementById('video');
            video.srcObject = stream;
            video.play();
        })
        .catch(function(err) {
            console.log("An error occurred: " + err);
        });

    // 拍照并将图像绘制到canvas
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, 640, 480);

    // 停止视频流
    video.srcObject.getTracks().forEach(track => track.stop());

    // 将图像转换为Base64字符串或Blob
    var image_data_url = canvas.toDataURL('image/png');

    // 发送到后端
    sendPhotoToBackend(image_data_url);
});

function sendPhotoToBackend(dataUrl) {
    // 这里使用 fetch API 发送数据到后端，你可以根据需要调整
    fetch('/your-backend-endpoint', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: dataUrl })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
