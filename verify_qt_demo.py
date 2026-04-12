#!/usr/bin/env python3
"""
Verify Qt demo automatically
"""

import subprocess
import time
import sys
import os

# Start the GUI process
print("Starting Qt demo verification...")
print("=" * 60)

# Try to run with different environment settings
process = subprocess.Popen(
    [sys.executable, "src/gui/main.py"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    cwd=".",
    env={**os.environ, "QT_QPA_PLATFORM": "offscreen"}
)

# Run for 5 seconds
try:
    start_time = time.time()
    while time.time() - start_time < 5:
        time.sleep(0.1)
        # Check if process is still running
        if process.poll() is not None:
            break
    
    # Terminate the process
    process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
    
    # Get output
    stdout, stderr = process.communicate()
    
    print("\nSTDOUT:")
    print(stdout)
    
    if stderr:
        print("\nSTDERR:")
        print(stderr)
    
    print("\n" + "=" * 60)
    print("Verification completed")
    print(f"Process exit code: {process.returncode}")
    
    # Save output to file
    with open("docs/contest_evidence/screenshots/17_qt_demo_verification.txt", "w") as f:
        f.write("Qt Demo Verification Output\n")
        f.write("=" * 60 + "\n")
        f.write("STDOUT:\n")
        f.write(stdout + "\n")
        if stderr:
            f.write("\nSTDERR:\n")
            f.write(stderr + "\n")
        f.write("\n" + "=" * 60 + "\n")
        f.write(f"Process exit code: {process.returncode}\n")
        f.write(f"Run time: {time.time() - start_time:.2f} seconds\n")
        
    print("Output saved to: docs/contest_evidence/screenshots/17_qt_demo_verification.txt")
    
except Exception as e:
    print(f"Error during verification: {e}")
