import gradio as gr
import os
import socket
from pathlib import Path
from config import SERVER_HOST, SERVER_PORT, STORAGE_DIR

def get_local_ip():
    """Get the local IP address of the machine"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("192.168.1.1", 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip

def list_files():
    """List all files in the current directory"""
    try:
        return [f.name for f in STORAGE_DIR.iterdir() if f.is_file()]
    except Exception as e:
        print(f"Error listing files: {e}")
        return []

def draw_files_dropdown():
    """Create a dropdown with the list of files"""
    return gr.Dropdown(
            choices=list_files(),
            label="Select file to download",
            interactive=True
        )

def upload_file(file):
    """Handle file upload"""
    if file is None:
        return "No file selected", draw_files_dropdown()
    
    try:
        file_path = STORAGE_DIR / Path(file.name).name  # Get just the filename
        # Copy the temporary file to our destination
        with open(file.name, 'rb') as src, open(file_path, 'wb') as dst:
            dst.write(src.read())
        return f"Successfully uploaded {file_path.name}", draw_files_dropdown()
    except PermissionError:
        return "Error: No permission to write file. Check directory permissions.", draw_files_dropdown()
    except Exception as e:
        return f"Error uploading file: {str(e)}", draw_files_dropdown()

def download_file(filename):
    """Handle file download"""
    if not filename:
        gr.Warning("No file selected")
        return None
        
    try:
        file_path = STORAGE_DIR / filename
        if not file_path.exists():
            gr.Warning(f"File {filename} not found")
            return None
        if not os.access(file_path, os.R_OK):
            gr.Warning(f"No permission to read file {filename}")
            return None
        return str(file_path)
    except Exception as e:
        gr.Warning(f"Error downloading file: {str(e)}")
        return None

with gr.Blocks(title="File Server") as demo:
    gr.Markdown("# File Server")
    gr.Markdown("Upload and download files easily")
    
    with gr.Column():
        # Upload section    
        gr.Markdown("Upload files")
        file_input = gr.File(label="Choose file to upload")
        upload_button = gr.Button("Upload")
        upload_status = gr.Textbox(label="Upload Status", interactive=False)

        # Download section
        gr.Markdown("Download files")    
        file_select = draw_files_dropdown()
        refresh_button = gr.Button("Refresh file list")
        download_button = gr.Button("Download")
        file_output = gr.File()

    # Set up event handlers
    upload_button.click(
        fn=upload_file,
        inputs=[file_input],
        outputs=[upload_status, file_select]
    )
    
    refresh_button.click(
        fn=draw_files_dropdown,
        inputs=None,
        outputs=file_select
    )
    
    download_button.click(
        fn=download_file,
        inputs=[file_select],
        outputs=file_output
    )

if __name__ == "__main__":
    local_ip = get_local_ip()
    print(f"Server is running and accessible via http://{local_ip}:{SERVER_PORT}/")
    demo.launch(
        server_name=SERVER_HOST,
        server_port=SERVER_PORT,
        share=False,
        allowed_paths=[STORAGE_DIR],
        show_error=True,  # Show detailed error messages
        debug=True  # Enable debug mode
    )
