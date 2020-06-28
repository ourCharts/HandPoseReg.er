const { app, BrowserWindow, Menu } = require('electron')
const net = require('net')
const ipc = require('electron').ipcMain
Menu.setApplicationMenu(null)

const sockConfig = {
  port: 6080,
  host: '127.0.0.1'
}
const sock = net.connect(sockConfig, function () {
  console.log('connected to server!')
})

sock.on('connect', function () {
  console.log('connect success')
})

function sendGesture(ges) {
  let ges2string = ges.toString()
  console.log(ges2string)
  sock.write(ges2string)
}

function createWindow() {
  const win = new BrowserWindow({
    width: 510,
    height: 200,
    alwaysOnTop: true,
    minimizable: false,
    frame: false,
    resizable: false,
    webPreferences: {
      nodeIntegration: true
    }
  })

  win.loadFile('index.html')

  // 打开开发者工具
  win.webContents.openDevTools()
}

app.whenReady().then(createWindow)
app.allowRendererProcessReuse = false

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})
process.env['ELECTRON_DISABLE_SECURITY_WARNINGS'] = 'true';


ipc.on('gesture', function (e, data) {
  console.log('gesture')
  sendGesture(data)
})

ipc.on('closewindow', e => app.quit())