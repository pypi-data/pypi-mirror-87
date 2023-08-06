import sys
import subprocess
import shlex

class Program:
    def __init__(self, command: str):
        self.command = command
        self.prepare_command()
        self.process = None
    def execute(self):
        is_windows = sys.platform.startswith('win')
        if is_windows:
            DETACHED_PROCESS = 0x00000008
            self.process = subprocess.Popen(shlex.split(self.command),creationflags=DETACHED_PROCESS,shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            self.process = subprocess.Popen(shlex.split(self.command))

    def prepare_command(self):
        return
