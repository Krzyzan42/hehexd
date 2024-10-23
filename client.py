import cv2
import random
import time
import pickle
import socket
from frame import FrameSegment, split_frame_into_segments

def xdd():
    server_address = ('localhost', 12345)
    message = b'Hello, Server!' 

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        print(f'Sending: {message.decode()}')
        s.sendto(message, server_address)

        data, server = s.recvfrom(4096)
        print(f'Received: {data.decode()} from {server}')

    except Exception as e:
        print(f"Error: {e}")

    s.close()

    server_address = ('localhost', 12345)  # Address to listen on
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    cam = cv2.VideoCapture(0)

    server_address = ('localhost', 12345)

    while True:
        ret, frame = cam.read()
        a = pickle.dumps(frame)
        cv2.imshow('test', frame)
        key = cv2.waitKey(1)
        if key%256 == 27:
            exit()

        s.sendto(frame, server_address)
        pass

def test_send_single_img():
    server_address = ('localhost', 12347)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cam = cv2.VideoCapture(0)

    frame_c = 0
    while True:
        _, frame = cam.read()
        #frame = cv2.resize(frame, (40, 30))

        segments = split_frame_into_segments(frame, frame_n=frame_c)
        frame_c += 1

        for i in range(len(segments)):
            s = segments[i]
            data = s.encode()
            sock.sendto(data, server_address)
        time.sleep(0.01)
            


if __name__ == '__main__':
    test_send_single_img()
