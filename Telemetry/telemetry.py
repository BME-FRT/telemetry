import serial
import socket

UDP_IP = "255.255.255.255"
UDP_PORT = 8998

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
interfaces = socket.getaddrinfo(host=socket.gethostname(), port=None, family=socket.AF_INET)
allips = [ip[-1][0] for ip in interfaces]
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

with serial.Serial('COM5', 230400, timeout=1) as ser:
    while True:
        try:
            startByte = ser.read()
            while startByte != b'\x7e':
                startByte = ser.read()
            message = ser.read(7)
            
            length = message[1]
            rssi = message[5]
            payload = ser.read(length - 5)
            print(rssi)
            for ip in allips:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                sock.bind((ip,0))
                sock.sendto(payload, (UDP_IP, UDP_PORT))
                sock.close()

        except:
            print("hupsz")
        