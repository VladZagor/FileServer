# FileServer

A simple web-based file server built with Gradio that allows you to easily share files between devices on your local network.

## Features

- Upload files through a web interface
- Download files with a single click (two clicks actually)
- Works on local network - access from any device

## Setup

1. Install dependencies:
```bash
pip install gradio
```

2. Configure the server:
- Edit `config.py` to set:
  - `SERVER_HOST` - server host address (default: "0.0.0.0")
  - `SERVER_PORT` - server port (default: 7860)
  - `STORAGE_DIR` - directory for file storage

3. Run the server:
```bash
python gradio_app/app.py
```

4. Access the web interface:
- The server will print the URL to access the interface
- Usually available at `http://YOUR_IP:7860`
- Can be accessed from any device on your local network

## Usage

1. **Upload Files**:
   - Click "Choose file to upload"
   - Select your file
   - Click "Upload"

2. **Download Files**:
   - Select a file from the dropdown list
   - Click "Download"
   - Click on file link below "Download" button

3. **Refresh File List**:
   - Click "Refresh file list" to update the list of available files