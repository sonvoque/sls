#|-------------------------------------------------------------------|
#| HCMC University of Technology                                     |
#| Telecommunications Departments                                    |
#| Wireless Embedded Firmware for Smart Lighting System (SLS)        |
#| Version: 2.0                                                      |
#| Author: sonvq@hcmut.edu.vn                                        |
#| Date: 01/2019                                                     |
#| - Client sw to control SLS via gateway                            |
#|-------------------------------------------------------------------|
#    
# Topology description:
#
#		|----------|     IPv6     |-----------|		 IPv4		|----------|
#		| 6LoWPAN  | ------------ |  Gateway  | --------------- | Client   |   
#		| network  |   wireless	  | + BR + DB |  wire/wireless  | software |
#		|----------|              |-----------|					|----------|
#


import socket
import binascii
import sys
import socket 
import time
from datetime import datetime

#static  char    dst_ipv6addr_list[20][50] ={"aaaa::212:4b00:5af:8406",
#											"aaaa::212:4b00:5af:8570",
#                                           "aaaa::212:4b00:5a9:8f83",
#                                           "aaaa::212:4b00:5a9:8fd5",                                     
#			   								"aaaa::212:4b00:5af:83f8",
#											"aaaa::212:4b00:5af:851f",
#											"aaaa::212:4b00:5af:8422",
#											"aaaa::212:4b00:5af:84dd",
#                                            "aaaa::212:4b00:5a9:8ff2",
#                                            "aaaa::212:4b00:5a9:8f91", 
#                                                                    };

GREEN = '\033[1;32m'
PINK  = '\033[1;35m'
RESET = '\033[0m'


#Socket to GW
UDP_IP 		= "127.0.0.1"
UDP_PORT 	= 21234

# IP of Gateway
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
MSG_TYPE_ASYNC			= 0x04


# for LED-driver
CMD_LED_PING			= 0x01
CMD_LED_SET_RTC			= 0x02
CMD_LED_RTC 			= 0x03
CMD_LED_MODE			= 0x04
CMD_LED_GET_STATUS      = 0x15
CMD_LED_EMERGENCY		= 0x06
CMD_LED_DIM				= 0x08
CMD_LED_SET_ID			= 0x0E
CMD_LED_GET_ID			= 0x0F


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

num_of_pkt_sent = 0
num_of_pkt_rev  = 0;

num_of_req_sent = 0
num_of_ack_rev  = 0
num_of_timout   = 0
total_delay 	= 0

print "\033[H\033[J"
print "Network topology"
print ""
print "		|----------|    IPv6    |-----------|      IPv4       "+PINK+"|----------|"+RESET
print "		| 6LoWPAN  |<---------->|  Gateway  |<--------------->"+PINK+"| Client   |"+RESET
print "		| network  |  wireless  | + BR + DB |  wire/wireless  "+PINK+"| software |"+RESET
print "		|----------|            |-----------|                 "+PINK+"|----------|"+RESET
print ""

#define number of iterations
max_num = 10

#loop of processing
for num in range(1,max_num+1):
	#make frame
	SFD 	= 0x7F
	len 	= 4			# node ID or IDs of multicast group
	seq1 	= 0x00
	seq0 	= num
	typ 	= MSG_TYPE_REQ
	cmd 	= CMD_RF_LED_DIM				#CMD_RF_LED_OFF    #CMD_GW_BROADCAST_CMD #CMD_GW_MULTICAST_CMD
	#cmd = 0xF6 + (num % 2)
	err1 	= 0x00
	err0 	= 0x00


	#define command executed on each node here
	multicast_cmd = CMD_RF_LED_DIM 			#CMD_RF_LED_DIM

	multicast_val1 = 2
	multicast_val2 = 0
	multicast_val3 = 0
	multicast_val4 = 0
	multicast_val5 = 0
	multicast_val6 = 0
	multicast_val7 = 0
	multicast_val8 = 0
	multicast_val9 = 0
	multicast_val10= 0


	#concat 64 bytes to a command
	MESSAGE = bytearray([SFD,len,seq1, seq0,typ, cmd, err1,err0, \
		multicast_cmd, \
		multicast_val1, multicast_val2, multicast_val3, multicast_val4, multicast_val5, \
		multicast_val6,multicast_val7, multicast_val8, multicast_val9, multicast_val10,\

		#addresses of multi-cast nodes
		2,3,4,0x00,0x00,0x00,0x00,0x00,0x00,\
		0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
		0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
		0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,\
		0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])


	BUFFER_SIZE = MAX_CMD_LEN
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))	
	old_millis = int(round(time.time() * 1000))
	print "--------------------------------------------------------"
	print "Client IP = ", host_ip
	print "Connect to 6LoWPAN-GW IP = " + GREEN, TCP_IP, RESET+", port: "+GREEN, TCP_PORT, ""+RESET
	print "--------------------------------------------------------"
	print "Time: ", datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
	print "Send REQUEST:" + PINK, num, RESET +" ",BUFFER_SIZE,"bytes"
	#print binascii.hexlify(MESSAGE) 
	print "len=", hex(MESSAGE[1]),"; seq=",hex(MESSAGE[2]),hex(MESSAGE[3]),"; type=",hex(MESSAGE[4]),"; cmd=",hex(MESSAGE[5]),"; err=",hex(MESSAGE[6]),hex(MESSAGE[7])
	print "data=[",
	for i in range(8,MAX_CMD_LEN):
		#print hex(MESSAGE[i]),
		print MESSAGE[i],
	print "]"
	s.send(MESSAGE)
	num_of_pkt_sent = num_of_pkt_sent +1

	
	data = s.recv(BUFFER_SIZE)
	s.close()
	new_millis = int(round(time.time() * 1000))
	print ""
	print "--------------------------------------------------------"
	print "Time: ",datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
	print "Received REPLY: ",BUFFER_SIZE, " bytes"
	num_of_pkt_rev = num_of_pkt_rev + 1

	#print binascii.hexlify(data) 
	reply = map(ord, data)
	#reply = list(data)
	print "len=", hex(reply[1]),"; seq=", hex(reply[2]), hex(reply[3]),"; type=", hex(reply[4]), "; cmd=", hex(reply[5]),"; err=",hex(reply[7]),hex(reply[6])
	print "data=[",
	for i in range(8,MAX_CMD_LEN):
		#print hex(reply[i]),
		print reply[i],
	print "]"
	print ""	
	print "Delay time = " + GREEN,new_millis-old_millis,RESET + "ms"

	total_delay = total_delay + (new_millis-old_millis)

	num_of_req_sent = num_of_req_sent + int(hex(reply[8]),0)
	num_of_ack_rev  = num_of_ack_rev  + int(hex(reply[9]),0)
	num_of_timout   = num_of_timout   + int(hex(reply[10]),0)

print ""
print "-----------------SUMMARY---------------------------------------"
print "Num of iteration = " + GREEN, num, RESET + ""
print "Num of packet sent/received = " + GREEN, num_of_pkt_sent, "/",num_of_pkt_rev, RESET + ""
print "Success rate (%) = " + GREEN, float(num_of_pkt_rev)*100/float(num_of_pkt_sent), RESET + ""
print "Average delay per pkt (ms) = ", total_delay/num_of_pkt_sent

if (cmd==CMD_GW_BROADCAST_CMD) or (cmd == CMD_GW_MULTICAST_CMD):
	print ""
	print "-------------SUMMARY BROADCAST/MULTICAST GW command------------"
	print "Num of request sent/received/time_out = " + GREEN ,num_of_req_sent,RESET + "/" + GREEN ,num_of_ack_rev, RESET + "/" + GREEN, num_of_timout, RESET + ""
	print "Success rate (%) = " + GREEN, float(num_of_ack_rev)*100/float(num_of_req_sent), RESET + ""
	print "---------------------------------------------------------------"