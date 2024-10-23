import socket
import matplotlib.pyplot as plt
import copy
from _pytest._code import Frame
import numpy as np
import cv2

from frame import FrameAssembler, FrameSegment

def udp_server():
    server_address = ('localhost', 12345)  # Address to listen on
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(server_address)

    # Bind the socket to the address
    print(f'Server listening on {server_address}')

    try:
        while True:
            print('\nWaiting for a message...')
            data, client_address = s.recvfrom(4096)
            print(f'Received: {data.decode()} from {client_address}')

            response = b'Hello, Client!'
            s.sendto(response, client_address)
            print(f'Sent: {response.decode()} back to {client_address}')
    except Exception as e:
        print(f'Error: {e}')

    s.close()

def test_mutliple_recvs():
    server_address = ('localhost', 12345)  # Address to listen on
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(server_address)

    input()

    while True:
        data, client_address = s.recvfrom(1000)
        print(f'Received: {data.decode()} from {client_address}')

def test_recv_frame():
    server_address = ('localhost', 12345)  # Address to listen on
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(server_address)
    s.setblocking(False)

    input()

    data, client_address = s.recvfrom(1000)
    frame = FrameSegment.decode(data)
    print(f'Received: {frame} from {client_address}')

def test_recv_multiple_frames():
    server_address = ('localhost', 12347)  # Address to listen on
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
            print(frame_n)
            last_n = frame_n

            cv2.imshow('hehexd', assembler.latest_frame)
            cv2.waitKey(1)
        


if __name__ == "__main__":
    test_recv_multiple_frames()

