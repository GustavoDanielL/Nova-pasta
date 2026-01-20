/**
 * FinancePro - Electron Preload Script
 * Provides secure bridge between renderer and main process
 */

const { contextBridge, ipcRenderer } = require('electron')

// Expose protected methods to the renderer process
contextBridge.exposeInMainWorld('electronAPI', {
    // App info
    getAppVersion: () => process.env.npm_package_version || '2.0.0',
    getPlatform: () => process.platform,
    
    // Theme
    getSystemTheme: () => {
        const { nativeTheme } = require('electron')
        return nativeTheme.shouldUseDarkColors ? 'dark' : 'light'
    },
    
    // Window controls (if needed for frameless window)
    minimizeWindow: () => ipcRenderer.send('window-minimize'),
    maximizeWindow: () => ipcRenderer.send('window-maximize'),
    closeWindow: () => ipcRenderer.send('window-close'),
    
    // Notifications
    showNotification: (title, body) => {
        new Notification(title, { body })
    },
    
    // File dialogs
    showSaveDialog: (options) => ipcRenderer.invoke('save-file-dialog', options),
    saveFile: (filePath, content, encoding) => ipcRenderer.invoke('save-file', { filePath, content, encoding })
})

// Log when preload is loaded
console.log('FinancePro preload script loaded')
