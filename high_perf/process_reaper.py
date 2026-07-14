from typing import List
import os
import signal
import time

class ProcessReaper:
    def __init__(self, target_app_name: str):
        self.target_app_name = target_app_name

    def scan_and_reap(self) -> List[int]:
        """
        Scans the system for zombie processes matching target_app_name,
        cleans them up, and returns a list of PIDs that were reaped.
        """
        reaped_pids = []

        try:
            proc_entries = os.scandir("/proc")
        except FileNotFoundError:
            return []

        with proc_entries as entries:
            for entry in entries:
                if entry.is_dir() and entry.name.isdigit():
                    pid = int(entry.name)
                    status_path = f"/proc/{pid}/status"
                    
                    # 1. Use defensive try/except blocks to handle processes 
                    # vanishing immediately during the read operations.
                    try:
                        with open(status_path, "r") as f:
                            name, state, ppid = None, None, None

                            for line in f:
                                if line.startswith("Name: "):
                                    name = line.split(":", 1)[1].strip()
                                elif line.startswith("State:"):
                                    state = line.split(":", 1)[1].strip()
                                elif line.startswith("PPid:"):
                                    ppid = int(line.split(":", 1)[1].strip())
                            
                            if name != self.target_app_name:
                                continue
                            if not state or not state.startswith("Z"):
                                continue
                            if ppid is None or ppid <= 1:
                                continue

                            os.kill(ppid, signal.SIGCHLD)
                            time.sleep(0.01)
                            
                            # If process remains ask parent pid to terminate 
                            if os.path.exists(f"/proc/{pid}"):
                                os.kill(ppid, signal.SIGTERM)
                                time.sleep(0.01)
                            
                            # Last check if process still exist then kill parent pid
                            if os.path.exists(f"/proc/{pid}"):
                                os.kill(ppid, signal.SIGKILL)

                            reaped_pids.append(pid)

                    except (FileNotFoundError, ProcessLookupError, PermissionError):
                        # Safely skip if process terminates or drops peivilages mid-scan
                        continue

        # Final loop verification checking if the entry successfully vanished
        # If process still exist then the ppid is in D (Uninterrubtable sleep) 
        # the kernel will not allow signal to reach it until it is unblocked from IO wait
        actually_reaped = []
        for pid in reaped_pids:
            if not os.path.exists(f"/proc/{pid}"):
                actually_reaped.append(pid)

        return actually_reaped