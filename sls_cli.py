import socket
import binascii

UDP_IP = "192.168.1.108"
UDP_PORT = 21234
SFD 	= 0x7F
len 	= 0x01
seq1 	= 0x01
seq0 	= 0x00
typ 	= 0x01
cmd 	= 0x01
err1 	= 0x00
err0 	= 0x00

MESSAGE = bytearray([SFD,len,seq1, seq0,typ, cmd, err1,err0, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
print "Send REQUEST:"
print binascii.hexlify(MESSAGE)

#sock.bind((UDP_IP, UDP_PORT))
while True:
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	print "received REPLY:"
	print binascii.hexlify(data)
	break