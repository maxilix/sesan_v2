import 		socket
import 		enum

from		constants 	import 		*




tracker = ("127.0.0.1",30304)

addressString 	= "0xea45041a6f49d1b4551861c9379fd7c475d22909"
enodeString 	= "enode://073d81a284a7579d2716c2efb0dbed1724208fcdd8e854ccfb552eab2f418e4b88a6cd6b658ef7aa6ca4b3db2d48ef395bc66528f2ffcf8c7a0bbef624064f39@127.0.0.1:30303"
#enodeString 	= "enode://eab1b8084f58259b812ec78f5f845429daf6ca9aefffffd8b54ef0af3c2ebaec05d955e984a22fbc583bf6d2d96cc98bcdb335add481c9232594f88ce1595238@127.0.0.1:30303"
nodekey 		= int(enodeString.split('@')[0][8:],16).to_bytes(64, byteorder='big')
ip 				= bytes([int(enodeString.split('@')[1].split(':')[0].split('.')[i]) for i in range(4)])
gethPort 		= int(enodeString.split('@')[1].split(':')[1]).to_bytes(2, byteorder='big')
enode 			= list(nodekey+ip+gethPort)
frame			= []


frame += [BC_BEGIN_IDENTITY]
frame += [BC_RECEIVED_ENODE]
frame += enode
frame += [BC_END_IDENTITY]



udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
#udpSocket.bind(('', CLIENT_PORT));

udpSocket.sendto(bytes(frame), tracker);


