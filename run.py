
import sys
import socket
import sonus

if __name__ == "__main__":
    if len(sys.argv) == 3:
        sonus.run(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 1:
        ip_addr = socket.gethostbyname(socket.getfqdn())
        sonus.run(ip_addr, 8000)
    else:
        raise Exception("Correct argument form not supplied")

