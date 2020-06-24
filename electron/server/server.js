const net = require('net')
const robot = require('robotjs')
let controlLock = false
// false: 可控制
// true: 不可控制

function altTab () {
  console.log('altTab')
  console.log(controlLock)
  if (controlLock === false) {
    controlLock = true
    robot.keyToggle('tab', 'down', 'alt')
    for (let i = 0; i < 4; i++) {
      robot.keyTap('tab')
    }
    robot.keyToggle('tab', 'up', 'alt')
    controlLock = false
  }
}

function audioDown () {
  console.log('audioDown')
  console.log(controlLock)
  if (controlLock === false) {
    controlLock = true
    for (let  i = 0; i < 10; i++) {
      robot.keyTap('audio_vol_down')
    }
    controlLock = false
  }
}

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
      altTab()
    } else if (stringifyData === '7') {
      audioDown()
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