const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');  // Node.js child_process to run Python script
const fs = require('fs');

function readJSONFile(filePath, callback) {
  // Read the JSON file asynchronously
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      callback(err, null);  // Return error through callback
      return;
    }

    try {
      const jsonData = JSON.parse(data);
      callback(null, jsonData);  // Return parsed JSON data through callback
    } catch (error) {
      callback(error, null);  // Return error if parsing fails
    }
  });
}

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
    // console.log(message['fanType'] + " " + message['numberOfPassengers'] + " " + message['range'])
    console.log(message)
    const pythonProcess = spawn('/Users/hawonc/Desktop/plain/venv3.11/bin/python', [path.join(__dirname, 'aircraft-models/matthew_labatory.py'), message['fanType'] + " " + message['numberOfPassengers'] + " " + message['range']]);

    pythonProcess.stdout.on('data', (data) => {
      // Send the output from Python script back to the renderer process
      event.reply('python-output', data.toString());
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Error: ${data}`);
    });

    pythonProcess.on('close', (code) => {
      console.log("done")
      if (code !== 0) {
        console.error(`Python script exited with code ${code}`);
      }
      readJSONFile('/Users/hawonc/Desktop/plain/aircraft-models/out.json', (err, data) => {
        if (err) {
          console.error('Error reading the JSON file:', err);
        } else {
          event.reply('donezo', JSON.stringify(data, null, 2));
        }
      });
    });
  });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
