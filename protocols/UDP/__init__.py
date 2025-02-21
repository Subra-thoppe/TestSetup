import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.abspath("."))

import socket, time
from modules import util

class UDP:

    def __init__(self, ip: str, port: int) -> None:
        util.typeCheck("ip", ip, str)
        util.typeCheck("port", port, int)

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.connect((ip, port))
        except Exception:
            util.errorCheck("VisaIOError", "ip", f"{ip}:{port}")
            
    def __read__(self, command: str) -> str:
        util.typeCheck("command", command, str)
        
        try:
            for _ in range(10):
                self.socket.send(str(command).encode())
                read = self.socket.recv(1024).decode()
                if read:
                    return str(read).strip()
        except Exception:
            util.errorCheck("VisaReadError", "UDP", command)
            time.sleep(0.5)

    def __write__(self, command: str) -> str:
        util.typeCheck("command", command, str)

        write = self.socket.send(str(command).encode())
        return str(write).strip()
    
    def __repr__(self) -> str:
        return "UDP Connection"