const robot = require("robotjs")
// // const sleep = require("sleep")
// robot.keyToggle('tab', 'down', 'alt')
// // sleep.sleep(1)
// for (let i = 0; i < 4; i++) {
//   //sleep.sleep(1)
//   robot.keyTap('tab')
// }
// // sleep.sleep(1)
// robot.keyToggle('tab', 'up', 'alt')

for (let i = 0; i < 10; i++) {
  robot.keyTap('audio_vol_down')
}