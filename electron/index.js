

const cv = require('./opencv.js');
let video = document.getElementById("video");
function getMedia() {
    let constraints = {
        video: {
            width: 400, height: 400, facingMode: 'user',
            mirrored: true
        },
        audio: false,
    };
    let promise = navigator.mediaDevices.getUserMedia(constraints);
    promise.then(function (MediaStream) {
        video.srcObject = MediaStream;
        video.play();
    }).catch(function (PermissionDeniedError) {
        console.log(PermissionDeniedError);
    });
}

var openCVonload = async function () {
    // const tf = require('@tensorflow/tfjs');
    const tf = require('@tensorflow/tfjs-node');
    // require('@tensorflow/tfjs-node')
    tf.setBackend('cpu');
    const model = await tf.loadLayersModel('./model.json');
    console.log(model);
    
    document.getElementById('status').innerHTML = 'opencv is ready';
    getMedia();
    setInterval(() => {
        // setTimeout(() => {
        let cap = new cv.VideoCapture(video);
        // 创建存放图像的Mat
        let src = new cv.Mat(video.height, video.width, cv.CV_8UC4);
        // 读一帧图像
        cap.read(src);
        // cv.imshow('canvasOutput', src);
        cv.flip(src, src, 1);
        let resize = new cv.Mat();
        let rect = new cv.Rect(300, 300, 400, 400);
        resize = src.roi(rect);
        cv.resize(resize, resize, new cv.Size(128, 128))
        let result = getSkin(resize);
        let two = fourier(result);
        cv.cvtColor(two, two, cv.COLOR_BGR2GRAY, 0);
        let arr = new Array();
        let out = [arr];

        for (var iter = 0; iter < 128; iter++) {
            let tmpArr = [];
            var strstr = "";
            for (var j = 0; j < 128; j++) {
                tmpArr.push([two.ucharAt(iter, j)]);
                strstr += two.ucharAt(iter, j) + ',';
            }
            // console.log(strstr)
            arr.push(tmpArr);
        }
        const tensor = tf.tensor(out);
        model.predict(tensor).print();
        // console.log(model.predict(out))
        // console.log(out);
        // console.log(two.channels());
        // console.log(two.depth());
        cv.imshow('canvasOutput1', result);
        cv.imshow('canvasOutput2', two);
        two.delete();
        result.delete();
        src.delete();
        resize.delete();
    }, 100);
}
function fourier(origin) {
    let tmp = origin.clone();
    cv.cvtColor(tmp, tmp, cv.COLOR_BGR2GRAY, 0);
    let tmp1 = tmp.clone();
    cv.Laplacian(tmp1, tmp1, cv.CV_16S, 3);
    cv.convertScaleAbs(tmp1, tmp1);
    let contours = new cv.MatVector();
    let hierarchy = new cv.Mat();
    cv.findContours(tmp, contours, hierarchy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    let final = new cv.Mat.zeros(origin.cols, origin.rows, cv.CV_8UC3);
    for (let i = 0; i < contours.size(); ++i) {
        let color = new cv.Scalar(255, 255, 255);
        cv.drawContours(final, contours, i, color, 1);
    }
    contours.delete();
    hierarchy.delete();
    tmp.delete();
    tmp1.delete();
    return final;
}
function getSkin(origin) {
    let tmp = origin.clone();
    cv.cvtColor(tmp, tmp, cv.COLOR_BGR2YCrCb, 0);
    let ycrcb_Planes = new cv.MatVector();
    cv.split(tmp, ycrcb_Planes);
    let cr = ycrcb_Planes.get(2);
    cv.GaussianBlur(cr, cr, new cv.Size(3, 3), 0, 0, cv.BORDER_DEFAULT);
    let skin = cr.clone();
    let result = tmp.clone();
    cv.threshold(cr, skin, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    cv.bitwise_and(origin, origin, result, skin);

    ycrcb_Planes.delete();
    cr.delete();
    skin.delete();
    tmp.delete();
    return result;
}