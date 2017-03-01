
#|-------------------------------------------------------------------|
#| HCMC University of Technology");                                  |
#| Telecommunications Departments                                    |
#| Python Programe interfacing with Gateway for SLS                  |
#| Version: 1.0                                                      |
#| Author: sonvq@hcmut.edu.vn                                        |
#| Date: 01/2017                                                     |
#|-------------------------------------------------------------------|


import socket
import binascii

#Socket to GW
UDP_IP 		= "192.168.1.108"
UDP_PORT 	= 21234

#Command
CMD_LED_OFF				= 0x01
CMD_LED_ON				= 0x02
CMD_LED_DIM				= 0x03
CMD_GET_LED_STATUS 		= 0x04
CMD_GET_NW_STATUS 		= 0x05
CMD_SET_APP_KEY			= 0x09
CMD_GET_APP_KEY			= 0x0A
CMD_LED_HELLO 			= 0x0B
CMD_LED_REBOOT			= 0x0C
CMD_GW_HELLO			= 0x0E


#msg type
MSG_TYPE_REQ			= 0x01
MSG_TYPE_REP			= 0x02
MSG_TYPE_HELLO			= 0x03


#make frame
SFD 	= 0x7F
len 	= 0x06		# node ID
seq1 	= 0x01
seq0 	= 0x00
typ 	= MSG_TYPE_REQ
cmd 	= CMD_LED_OFF
err1 	= 0x00
err0 	= 0x00
MESSAGE = bytearray([SFD,len,seq1, seq0,typ, cmd, err1,err0, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])


#send COMMAND
print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
print "Send REQUEST:"
print binascii.hexlify(MESSAGE)

#receive REPLY
#sock.bind((UDP_IP, UDP_PORT))
while True:
	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
	print "received REPLY:"
	print binascii.hexlify(data)
	break