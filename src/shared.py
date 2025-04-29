import threading
import io

shared_output = io.StringIO()
output_lock = threading.Lock()

# clears the shared_output string
def reset_shared_output():
    global shared_output
    shared_output = io.StringIO()
