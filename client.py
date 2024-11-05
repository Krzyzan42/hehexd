import cv2
import sys
import socket
from frame import split_frame_into_segments

def run_client(host, port):
    server_address = (host, int(port))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cam = cv2.VideoCapture(0)

    frame_c = 0
    while True:
        _, frame = cam.read()
        #frame = cv2.resize(frame, (1980, 1024))

        segments = split_frame_into_segments(frame, frame_n=frame_c)
        frame_c += 1

        for i in range(len(segments)):
            s = segments[i]
            data = s.encode()
            sock.sendto(data, server_address)


if __name__ == '__main__':
    run_client(sys.argv[1], sys.argv[2])
