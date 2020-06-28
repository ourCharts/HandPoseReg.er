const net = require('net')
const robot = require('robotjs')
let controlable = false//解锁
let directable = false//开启上下左右键
let key_set = []
function clear_key() {
  for (let index = 0; index < key_set.length; index++) {
    robot.keyToggle(key_set[index], 'up');
  }
  key_set = []
}

function minimize() {
  console.log('minimize')
  pre_gesture = 7;
  robot.keyToggle('command', 'down')
  robot.keyTap('D')
  robot.keyToggle('command', 'up')

}
function closeWindow() {
  console.log('closeWin')
  pre_gesture = 4;
  robot.keyToggle('alt', 'down')
  robot.keyTap('f4')
  robot.keyToggle('alt', 'up')
  
}
function altTab() {
  console.log('altTab')
  pre_gesture = 8;
  robot.keyToggle('alt', 'down')
  key_set.push('alt')
  robot.keyTap('tab')
}
function re_altTab() {
  console.log('re_altTab')
  pre_gesture = 9;
  robot.keyToggle('alt', 'down')
  key_set.push('alt')
  robot.keyToggle('shift', 'down')
  key_set.push('shift')
  robot.keyTap('tab')
}
function audioMute() {
  console.log('audio_mute')
  robot.keyTap('audio_mute');
}

let pre_gesture;
const server = net.createServer(function (sock) {
  sock.on('close', function () {
    console.log('close socket')
    server.close()
  })
  sock.on('data', function (data) {
    console.log('ok!')
    console.log(data.toString())
    let stringifyData = data.toString()
    if (stringifyData === '5') {
      directable = false;
      if (controlable) {
        controlable = false;
        clear_key();
      }
      else {
        controlable = true;
      }
      pre_gesture = stringifyData;
    }
    if (controlable) {
      if (directable) {
        if (stringifyData === '1') {
          console.log('up')
          robot.keyTap('up')
        }
        else if (stringifyData === '7') {
          console.log('down')
          robot.keyTap('down')
        }
        else if (stringifyData === '8') {
          console.log('right')
          robot.keyTap('right')
        }
        else if (stringifyData === '9') {
          console.log('left')
          robot.keyTap('left')
        }
      }
      else {
        if (stringifyData != pre_gesture) {
          clear_key()
        }
        if (stringifyData === '6') {
          audioMute()
        }
        else if (stringifyData === '7') {
          minimize()
        }
        else if (stringifyData === '4') {
          directable = true;
        }
        else if (stringifyData === '2') {
          closeWindow()
        }
        else if (stringifyData === '9') {
          re_altTab()
        }
        else if (stringifyData === '8') {
          altTab()
        }
      }
    }
  })
})

server.on('listening', function () {
  console.log('start listening')
})

server.on('error', function () {
  console.log('listen error')
})

server.on('close', function () {
  console.log('stop listening')
})

server.listen({
  port: 6080,
  host: '127.0.0.1',
  exclusive: true
})