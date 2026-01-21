const { app, BrowserWindow, Menu, shell, nativeTheme, ipcMain, dialog } = require('electron')
const path = require('path')
const { spawn, exec } = require('child_process')
const net = require('net')
const fs = require('fs')

let backendProcess = null
let mainWindow = null

// Configure app for better Linux compatibility
if (process.platform === 'linux') {
  app.commandLine.appendSwitch('disable-gpu-sandbox')
}

// Check if a port is available
function isPortAvailable(port) {
  return new Promise((resolve) => {
    const server = net.createServer()
    server.once('error', () => resolve(false))
    server.once('listening', () => {
      server.close()
      resolve(true)
    })
    server.listen(port, '127.0.0.1')
  })
}

async function startBackend() {
  // First check if backend is already running
  const portAvailable = await isPortAvailable(8000)
  if (!portAvailable) {
    console.log('Backend already running on port 8000')
    return
  }

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

      console.log('Backend process started (bundled)')
    } catch (e) {
      console.error('Erro ao iniciar backend empacotado:', e)
    }
  } else {
    // Allow override of python executable via env var
    const pythonCmd = process.env.FINANCEPRO_PYTHON || 'python3' || 'python'
    // Start uvicorn as subprocess
    try {
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

    console.log('Backend process started (python)')
  }
}

function stopBackend() {
  if (backendProcess) {
    try {
      // Try graceful termination first
      if (process.platform === 'win32') {
        spawn('taskkill', ['/pid', backendProcess.pid, '/f', '/t'])
      } else {
        backendProcess.kill('SIGTERM')
        // Force kill after timeout
        setTimeout(() => {
          if (backendProcess) {
            backendProcess.kill('SIGKILL')
          }
        }, 2000)
      }
    } catch (e) {
      console.error('Erro ao matar backend:', e)
    }
    backendProcess = null
  }
}

function createMenu() {
  const template = [
    {
      label: 'Arquivo',
      submenu: [
        { label: 'Recarregar', accelerator: 'CmdOrCtrl+R', click: () => mainWindow?.reload() },
        { type: 'separator' },
        { label: 'Sair', accelerator: 'CmdOrCtrl+Q', click: () => app.quit() }
      ]
    },
    {
      label: 'Editar',
      submenu: [
        { role: 'undo', label: 'Desfazer' },
        { role: 'redo', label: 'Refazer' },
        { type: 'separator' },
        { role: 'cut', label: 'Cortar' },
        { role: 'copy', label: 'Copiar' },
        { role: 'paste', label: 'Colar' },
        { role: 'selectAll', label: 'Selecionar Tudo' }
      ]
    },
    {
      label: 'Visualização',
      submenu: [
        { role: 'resetZoom', label: 'Zoom Normal' },
        { role: 'zoomIn', label: 'Aumentar Zoom' },
        { role: 'zoomOut', label: 'Diminuir Zoom' },
        { type: 'separator' },
        { role: 'togglefullscreen', label: 'Tela Cheia' }
      ]
    },
    {
      label: 'Ajuda',
      submenu: [
        {
          label: 'Sobre FinancePro',
          click: async () => {
            const { dialog } = require('electron')
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'Sobre FinancePro',
              message: 'FinancePro v2.0.0',
              detail: 'Sistema de Gestão de Empréstimos\n\n© 2024-2026 FinancePro\nTodos os direitos reservados.'
            })
          }
        },
        { type: 'separator' },
        {
          label: 'DevTools',
          accelerator: 'F12',
          click: () => mainWindow?.webContents.toggleDevTools()
        }
      ]
    }
  ]

  const menu = Menu.buildFromTemplate(template)
  Menu.setApplicationMenu(menu)
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1024,
    minHeight: 700,
    icon: path.join(__dirname, 'assets', 'icon.png'),
    backgroundColor: '#f8fafc',
    show: false, // Don't show until ready
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: true
    }
  })

  // Show window when ready to prevent visual flash
  mainWindow.once('ready-to-show', () => {
    mainWindow.show()
  })

  // Handle external links
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url)
    return { action: 'deny' }
  })

  mainWindow.loadFile(path.join(__dirname, 'index.html'))
  
  // Handle window close
  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

// IPC handlers for file dialogs
ipcMain.handle('save-file-dialog', async (event, { title, defaultPath, filters }) => {
  const result = await dialog.showSaveDialog(mainWindow, {
    title: title || 'Salvar arquivo',
    defaultPath: defaultPath || 'arquivo',
    filters: filters || [{ name: 'Todos os arquivos', extensions: ['*'] }]
  })
  return result
})

ipcMain.handle('save-file', async (event, { filePath, content, encoding }) => {
  try {
    fs.writeFileSync(filePath, content, encoding || 'utf8')
    return { success: true }
  } catch (error) {
    return { success: false, error: error.message }
  }
})

app.whenReady().then(async () => {
  // Start backend before creating the window
  await startBackend()
  
  // Create menu
  createMenu()

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
