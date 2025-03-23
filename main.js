const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');  // Node.js child_process to run Python script

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false, // Allow Node.js access to frontend
      webSecurity: false,  // Disabling security (only for local dev, not production)
    }
  });

  win.loadFile('index.html');  // Your HTML file

  // When a request to run Python is received, execute the Python script
  ipcMain.on('run-python', (event, message) => {
    // Execute your Python script and pass the user input as argument
    const pythonProcess = spawn('python', [path.join(__dirname, 'your_script.py'), message]);

    pythonProcess.stdout.on('data', (data) => {
      // Send the output from Python script back to the renderer process
      event.reply('python-output', data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        console.error(`Python script exited with code ${code}`);
      }
    });
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
