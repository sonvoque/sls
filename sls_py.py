import socket
import binascii


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
CMD_SET_APP_KEY			= 0xF1
CMD_GET_APP_KEY			= 0xF0
CMD_RF_REBOOT			= 0xEF
CMD_RF_REPAIR_ROUTE		= 0xEE
CMD_GW_SET_TIMEOUT		= 0xED

CMD_TEST_TIMEOUT		= 0xCD
CMD_GW_MULTICAST_CMD	= 0xEC

#msg type
MSG_TYPE_REQ			= 0x01
MSG_TYPE_REP			= 0x02
MSG_TYPE_HELLO			= 0x03


#make frame
SFD 	= 0x7F
len 	= 3		# node ID
seq1 	= 0x01
seq0 	= 0x00
typ 	= MSG_TYPE_REQ
cmd 	= CMD_GW_MULTICAST_CMD
err1 	= 0x00
err0 	= 0x00
multicast_val1 = 20
multicast_val2 = 0
multicast_cmd = CMD_RF_LED_OFF
MESSAGE = bytearray([SFD,len,seq1, seq0,typ, cmd, err1,err0, multicast_cmd, multicast_val1,multicast_val2,10,11,1,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])


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