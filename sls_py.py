import socket
import binascii
import sys
import socket 
import time
from datetime import datetime


#from __future__ import print_function

#static  char    dst_ipv6addr_list[20][50] ={"aaaa::212:4b00:5af:8406",
#											"aaaa::212:4b00:5af:8570",
#                                           "aaaa::212:4b00:5a9:8f83",
#                                          	"aaaa::212:4b00:5a9:8fd5",                                              
#			   								"aaaa::212:4b00:5af:83f8",
#											"aaaa::212:4b00:5af:851f",
#											"aaaa::212:4b00:5af:8422",
#											"aaaa::212:4b00:5af:84dd",
#                                            "aaaa::212:4b00:5a9:8ff2",
#                                            "aaaa::212:4b00:5a9:8f91", 
#                                                                    };


#Socket to GW
UDP_IP 		= "127.0.0.1"
UDP_PORT 	= 21234

#TCP_IP = "192.168.144.150"
TCP_IP = "127.0.0.1"
TCP_PORT = 21234

MAX_CMD_LEN	= 64	

#Command
CMD_GET_RF_STATUS 		= 0xFF
CMD_GET_NW_STATUS 		= 0xFE
CMD_GET_GW_STATUS 		= 0xFD
CMD_GW_HELLO			= 0xFC
CMD_GW_SHUTDOWN			= 0xFB
CMD_GW_TURN_ON_ALL		= 0xFA
CMD_GW_TURN_OFF_ALL		= 0xF9
CMD_GW_DIM_ALL			= 0xF8
CMD_RF_LED_OFF			= 0xF7
CMD_RF_LED_ON			= 0xF6
CMD_RF_LED_DIM			= 0xF5
CMD_RF_HELLO 			= 0xF4
CMD_RF_TIMER_ON 		= 0xF3
CMD_RF_TIMER_OFF 		= 0xF2
CMD_RF_SET_APP_KEY		= 0xF1
CMD_RF_GET_APP_KEY		= 0xF0
CMD_RF_REBOOT			= 0xEF
CMD_RF_REPAIR_ROUTE		= 0xEE
CMD_GW_SET_TIMEOUT		= 0xED

CMD_TEST_TIMEOUT		= 0xCD
CMD_GW_MULTICAST_CMD	= 0xEC
CMD_GW_BROADCAST_CMD	= 0xEB
CMD_GW_GET_EMER_INFO	= 0xEA
CMD_GW_TURN_ON_ODD		= 0xE9
CMD_GW_TURN_ON_EVEN		= 0xE8
CMD_GW_TURN_OFF_ODD		= 0xE7
CMD_GW_TURN_OFF_EVEN	= 0xE6
CMD_GW_DIM_ODD			= 0xE5
CMD_GW_DIM_EVEN			= 0xE4
CMD_GW_RELOAD_FW		= 0xE3

#msg type
MSG_TYPE_REQ			= 0x01
MSG_TYPE_REP			= 0x02
MSG_TYPE_HELLO			= 0x03


#make frame
SFD 	= 0x7F
len 	= 1			# node ID or IDs of multicast group
seq1 	= 0x00
seq0 	= 0x01
typ 	= MSG_TYPE_REQ
cmd 	= CMD_GW_BROADCAST_CMD    #CMD_GW_BROADCAST_CMD #CMD_GW_MULTICAST_CMD
err1 	= 0x00
err0 	= 0x00


#define command executed on each node here
multicast_cmd = CMD_RF_LED_DIM 			#CMD_RF_LED_DIM

multicast_val1 = 20
multicast_val2 = 0
multicast_val3 = 0
multicast_val4 = 0
multicast_val5 = 0
multicast_val6 = 0
multicast_val7 = 0
multicast_val8 = 0
multicast_val9 = 0
multicast_val10 = 0


#64 bytes command
MESSAGE = bytearray([SFD,len,seq1, seq0,typ, cmd, err1,err0, \
	multicast_cmd, \
	multicast_val1, multicast_val2, multicast_val3, multicast_val4, multicast_val5, multicast_val6,\
	multicast_val7, multicast_val8, multicast_val9, multicast_val10,\

	#addresses of multi-cast nodes
	25,9,10,0x00,0x00,0x00,0x00,0x00,0x00,\
	0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
	0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
	0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
	0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])


#send COMMAND
#print "UDP target IP:", UDP_IP
#print "UDP target port:", UDP_PORT
#sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
#print "Send REQUEST:"
#print binascii.hexlify(MESSAGE)

#receive REPLY
#sock.bind((UDP_IP, UDP_PORT))
#while True:
#	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
#	print "received REPLY:"
#	print binascii.hexlify(data)
#	break

host_name = socket.gethostname() 
host_ip = socket.gethostbyname(host_name) 

max_num = 1
for num in range(1,max_num+1):
	BUFFER_SIZE = MAX_CMD_LEN
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))	
	old_millis = int(round(time.time() * 1000))
	print "--------------------------------------------------------"
	print "Client IP = ", host_ip
	print "Connect to 6LoWPAN-GW IP = ",TCP_IP,",port: ", TCP_PORT
	print "--------------------------------------------------------"
	print "Time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
	print "Send REQUEST:", num,": ", BUFFER_SIZE, " bytes"
	print binascii.hexlify(MESSAGE) 
	print "len=", hex(MESSAGE[1]),"; seq=",hex(MESSAGE[2]),hex(MESSAGE[3]),"; type=",hex(MESSAGE[4]),"; cmd=",hex(MESSAGE[5]),"; err=",hex(MESSAGE[6]),hex(MESSAGE[7])
	print "data=[",
	for i in range(8,MAX_CMD_LEN):
		print hex(MESSAGE[i]),
	print "]"
	s.send(MESSAGE)

	
	data = s.recv(BUFFER_SIZE)
	s.close()
	new_millis = int(round(time.time() * 1000))
	print ""
	print "--------------------------------------------------------"
	print "Time: ",datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
	print "Received REPLY: ",BUFFER_SIZE, " bytes"
	print binascii.hexlify(data) 
	reply = map(ord, data)
	#reply = list(data)
	print "len=", hex(reply[1]),"; seq=", hex(reply[2]), hex(reply[3]),"; type=", hex(reply[4]), "; cmd=", hex(reply[5]),"; err=",hex(reply[7]),hex(reply[6])
	print "data=[",
	for i in range(8,MAX_CMD_LEN):
		print hex(reply[i]),
	print "]"
	print ""	
	print "Delay time = ",new_millis-old_millis,"ms"