from dataclasses import dataclass
import cv2
import numpy as np

MAX_PAYLOAD_SIZE = 500

@dataclass
class FrameSegment:
    frame_num :int
    segment_num :int
    payload :bytes
    is_last :bool

    def encode(self):
        a = self.frame_num.to_bytes(16, byteorder='big')
        b = self.segment_num.to_bytes(16, byteorder='big')
        c = self.is_last.to_bytes(1, byteorder='big')
        d = self.payload

        return  a + b + c + d

    @staticmethod
    def decode(byte_array):
        frame_n = int.from_bytes(byte_array[:16], byteorder='big')
        segment_num = int.from_bytes(byte_array[16:32], byteorder='big')
        is_last = bool.from_bytes([byte_array[32]], byteorder='big')
        payload = byte_array[33:]

        return FrameSegment(frame_n, segment_num, payload, is_last)

    def __str__(self) -> str:
        return f'{self.frame_num}:{self.segment_num}:{self.is_last}'

def split_frame_into_segments(img :np.ndarray, frame_n = 0, paylaod_size=500):
    encoded = cv2.imencode('.png', img)[1].tobytes()
    segment_data :list[bytes] = []
    for i in range(0, len(encoded), paylaod_size):
        segment_data.append(encoded[i:i+paylaod_size])

    segments :list[FrameSegment] = []
    for i in range(len(segment_data)):
        segments.append(FrameSegment(frame_n, i, segment_data[i], False))
    segments[-1].is_last = True
    print(segments[-1].frame_num)
    return segments

class LoadingFrame:
    found_last :bool
    segment_dump :list
    ordered_segments :list

    found_count :int
    expected_count :int | None

    def __init__(self) -> None:
        self.found_last = False
        self.segment_dump = []
        self.ordered_segments = []
        self.found_count = 0
        self.expected_count = None

    def recv_segment(self, segment :FrameSegment):
        if self.found_last:
            self.ordered_segments[segment.segment_num] = segment
        else:
            self.segment_dump.append(segment)
            if segment.is_last:
                self.found_last = True
                self.expected_count = segment.segment_num + 1
                self._reorder_dump(segment)

        self.found_count += 1

    def _reorder_dump(self, last_seg :FrameSegment):
        self.ordered_segments = [None] * (last_seg.segment_num + 1)
        for s in self.segment_dump:
            self.ordered_segments[s.segment_num] = s

    def is_done(self):
        return self.found_count == self.expected_count

class FrameAssembler:
    frames :dict[int, LoadingFrame]

    def __init__(self) -> None:
        self.frames = {}
        self.latest_frame_n = -1
        self.latest_frame = None

    def get_latest_frame(self):
        return self.latest_frame_n

    def recv_frame_segment(self, segment :FrameSegment):
        if segment.frame_num not in self.frames:
            self.frames[segment.frame_num] = LoadingFrame()
        frame = self.frames[segment.frame_num]
        frame.recv_segment(segment)

        if frame.is_done():
            print(f'Completed {segment.frame_num}')
            self.frames.pop(segment.frame_num)
            print(f'Processing {len(self.frames)} frames')
            if segment.frame_num > self.latest_frame_n:
                self.latest_frame_n = segment.frame_num
                self.latest_frame = self._assemble(frame)

    def _clear_old_frames(self, below_frame):
        for i in range(below_frame-1):
            if i in self.frames:
                self.frames.pop(i)

    def _assemble(self, frame):
        bytes_array = [b''] * (frame.found_count)
        for s in frame.ordered_segments:
            bytes_array[s.segment_num] = s.payload

        joined_byte_array = []
        for payload in bytes_array:
            joined_byte_array.extend(payload)
            
        nparr = np.frombuffer(bytes(joined_byte_array), dtype=np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        return img



