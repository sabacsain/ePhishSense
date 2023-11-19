# scan.py

import sys
import json

def run_scan():
    # Your scanning logic here
    result = "Scan completed"

    # Send the result back to the extension
    print(json.dumps({"result": result}))
    sys.stdout.flush()

if __name__ == "__main__":
    run_scan()
