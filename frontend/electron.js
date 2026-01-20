const { app, BrowserWindow } = require('electron')
const path = require('path')
const { spawn } = require('child_process')

let backendProcess = null

function startBackend(){
  // Prefer bundled backend binary when available (resources/backend/financepro-backend)
  const bundled = path.join(__dirname, '..', 'resources', 'backend', process.platform === 'win32' ? 'financepro-backend.exe' : 'financepro-backend')
  if (require('fs').existsSync(bundled)) {
    try {
      backendProcess = spawn(bundled, [], {
        cwd: path.join(__dirname, '..'),
        env: process.env,
        stdio: ['ignore', 'pipe', 'pipe']
      })

      if (backendProcess) {
        backendProcess.stdout.on('data', (data) => {
          console.log(`[backend] ${data.toString()}`)
        })
        backendProcess.stderr.on('data', (data) => {
          console.error(`[backend][err] ${data.toString()}`)
        })

        backendProcess.on('close', (code) => {
          console.log(`Backend exited with code ${code}`)
          backendProcess = null
        })
      }

      console.log('Backend process started')
    } catch (e) {
      console.error('Erro ao iniciar backend empacotado:', e)
    }
  } else {
    // Allow override of python executable via env var
    const pythonCmd = process.env.FINANCEPRO_PYTHON || 'python'
    // Start uvicorn as subprocess
    try{
      backendProcess = spawn(pythonCmd, ['-m', 'uvicorn', 'backend.api:app', '--host', '127.0.0.1', '--port', '8000'], {
        cwd: path.join(__dirname, '..'),
        env: process.env,
        stdio: ['ignore', 'pipe', 'pipe']
      })
    } catch (e) {
      console.error('Erro ao iniciar backend via python:', e)
    }

    if (backendProcess) {
      backendProcess.stdout.on('data', (data) => {
        console.log(`[backend] ${data.toString()}`)
      })
      backendProcess.stderr.on('data', (data) => {
        console.error(`[backend][err] ${data.toString()}`)
      })

      backendProcess.on('close', (code) => {
        console.log(`Backend exited with code ${code}`)
        backendProcess = null
      })
    }

    console.log('Backend process started')
  }

}

function stopBackend(){
  if(backendProcess){
    try{
      backendProcess.kill()
    }catch(e){
      console.error('Erro ao matar backend:', e)
    }
  }
}

function createWindow () {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, 'renderer.js'),
      nodeIntegration: false,
      contextIsolation: true
    }
  })

  win.loadFile(path.join(__dirname, 'index.html'))
}

app.whenReady().then(() => {
  // Start backend before creating the window
  startBackend()

  createWindow()

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('before-quit', () => {
  // Ensure backend is terminated when app quits
  stopBackend()
})

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    stopBackend()
    app.quit()
  }
})
