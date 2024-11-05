import socket
import sys
import cv2

from frame import FrameAssembler, FrameSegment

def run_server(host, port):
    server_address = (host, int(port))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(server_address)
    assembler = FrameAssembler()

    last_n = -1
    while True:
        data, _ = s.recvfrom(1000)
        frame = FrameSegment.decode(data)
        assembler.recv_frame_segment(frame)

        frame_n = assembler.get_latest_frame()
        if last_n != frame_n and frame_n is not None:
            last_n = frame_n

            cv2.imshow('hehexd', assembler.latest_frame)
            cv2.waitKey(1)

if __name__ == "__main__":
    run_server(sys.argv[1], sys.argv[2])

