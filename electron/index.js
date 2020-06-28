const cv = require('./opencv.js');
let video = document.getElementById("video");
let Switch = false;
const messageDiv = document.getElementById('Message')

function getMedia() {
  let constraints = {
    video: {
      width: 400, 
      height: 400, 
      facingMode: 'user',
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


let count = 0;
let gesture_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0]
let controlLock = true;
const openCVonload = async function () {
  // const tf = require('@tensorflow/tfjs');
  const tf = require('@tensorflow/tfjs');
  // require('@tensorflow/tfjs-node')
  // tf.setBackend('cpu');
  const model = await tf.loadLayersModel('./model.json');
  let preGes = -1;
  let curGes = -1;
  let sameGesCnt = 0;

  // document.getElementById('status').innerHTML = 'opencv is ready';
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
      arr.push(tmpArr);
    }
    let predictResult = model.predict(tf.tensor(out));
    predictResult.data().then(res => {
      let array = Object.values(res);
      let maximum = -1;
      let maxiidx = 0;
      for (let idx = 0; idx < array.length; idx++) {
        if (maximum < array[idx]) {
          maximum = array[idx];
          maxiidx = idx;
        }
      }

      let gesture = maxiidx;
      gesture_arr[gesture]++;
      count++;
      if (count >= 10) {
        gesture, max_count = max_gesture();
        if (max_count > 8) {
          gesture += 1;
          if (gesture == 5) {
            if (controlLock) {
              lock(false);
              controlLock = false;
            } else {
              lock(true);
              controlLock = true;
            }
          }
          console.log('手势：' + gesture);
          messageDiv.innerHTML = 'Give me your gesture 😊'
          ipc.send('gesture', gesture);
        } else {
          console.log('请调整好手势');
          messageDiv.innerHTML = 'Please adjust your gesture 🤔'
        }
        clear();
        count = 0;
      }
    });
    // cv.imshow('canvasOutput1', result);
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

function lock(flag) {
  if (flag) {
    document.getElementById('lockStatus').innerHTML = '🔒 Locked';
  }
  else {
    document.getElementById('lockStatus').innerHTML = '🔓 Unlocked';
  }
}

function clear() {
  gesture_arr = [0, 0, 0, 0, 0, 0, 0, 0, 0];
}

function max_gesture() {
  let max = -1; let gesture_idx = -1;
  for (let index = 0; index < gesture_arr.length; index++) {
    const element = gesture_arr[index];
    if (max < element) {
      max = element;
      gesture_idx = index;
    }
  }
  return gesture_idx, max;
}

document.getElementById('closeWindow').addEventListener('click', function () {
  // ipc.send('closewindow')
  console.log('debug1')
})