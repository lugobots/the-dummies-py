import subprocess
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define the command to start your server
server_command = "python main.py"

# Define the directory to watch for changes
watched_directory = "./"

# Define a flag to check if the server is running
server_running = False


# Function to start the server
def start_server():
    global server_running
    if not server_running:
        print("Starting the server...")
        subprocess.Popen(server_command, shell=True)
        server_running = True


# Function to stop the server
def stop_server():
    global server_running
    if server_running:
        print("Stopping the server...")
        os.system("pkill -f main.py")
        server_running = False


# Define an event handler for file changes
class ServerReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"Detected changes in {event.src_path}")
            stop_server()
            start_server()


# Create an observer to watch the directory
observer = Observer()
event_handler = ServerReloadHandler()
observer.schedule(event_handler, path=watched_directory, recursive=True)
observer.start()

try:
    start_server()  # Start the server initially
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
