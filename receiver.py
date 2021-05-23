import socket
import struct
import cv2
import numpy as np
import sys
import math

MAX_DGRAM = 2**16

def dump_buffer(s):
	while 1:
		seg, addr = s.recvfrom(MAX_DGRAM)
		print(seg[0])
		if struct.unpack("B", seg[0:1])[0] == 1:
			print("\nfinish emptying buffer")
			break

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('localhost', 12345))
dat = b""
dump_buffer(s) 
while True:
	seg, addr = s.recvfrom(MAX_DGRAM)
	if struct.unpack('B', seg[0:1])[0] > 1:
		dat += seg[1:]
	else:
		dat += seg[1:]
		img = cv2.imdecode(np.fromstring(dat, dtype=np.uint8), 1)
		cv2.imshow('frame', img)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		dat = b"" # cap.release()
cv2.destroyAllWindows()
s.close()