#!/usr/bin/env python3
"""
Emergency script to kill stuck teleprompter processes
"""

import os
import subprocess
import signal

def kill_python_processes():
    """Kill all Python processes related to the teleprompter"""
    try:
        # Find Python processes
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        python_pids = []
        for line in lines:
            if 'python' in line.lower() and ('interview' in line or 'teleprompter' in line or 'gui.py' in line or 'core.py' in line):
                parts = line.split()
                if len(parts) > 1:
                    try:
                        pid = int(parts[1])
                        python_pids.append(pid)
                        print(f"🎯 Found Python process: PID {pid} - {line}")
                    except ValueError:
                        continue
        
        if not python_pids:
            print("✅ No teleprompter Python processes found")
            return
        
        # Kill the processes
        for pid in python_pids:
            try:
                print(f"🔪 Killing process {pid}...")
                os.kill(pid, signal.SIGTERM)  # Try graceful termination first
            except ProcessLookupError:
                print(f"⚠️  Process {pid} already terminated")
            except PermissionError:
                print(f"❌ Permission denied to kill process {pid}")
                
        # Wait a bit and force kill if needed
        import time
        time.sleep(2)
        
        for pid in python_pids:
            try:
                os.kill(pid, signal.SIGKILL)  # Force kill
                print(f"💀 Force killed process {pid}")
            except ProcessLookupError:
                pass  # Already dead
            except PermissionError:
                print(f"❌ Permission denied to force kill process {pid}")
                
        print("🧹 Cleanup complete!")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")

if __name__ == "__main__":
    print("🚨 Emergency Teleprompter Killer")
    print("This will terminate all teleprompter-related Python processes")
    
    confirm = input("Are you sure? (y/N): ").strip().lower()
    
    if confirm == 'y':
        kill_python_processes()
    else:
        print("🛑 Cancelled")
