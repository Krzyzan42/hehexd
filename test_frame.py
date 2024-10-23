from frame import FrameAssembler, FrameSegment
import pytest

def test_frame_segment():
    frame = FrameSegment(1234, 9876, b'payload hehexd', True)
    frame_bytes = frame.encode()
    frame_decoded = FrameSegment.decode(frame_bytes)

    assert frame_decoded.frame_num == 1234
    assert frame_decoded.segment_num == 9876
    assert frame_decoded.payload == b'payload hehexd'
    assert frame_decoded.is_last == True


class TestFrameAssembler:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.frame_assembler = FrameAssembler()

    def assert_segments_produce(self, segments, output):
        for s in segments:
            self.frame_assembler.recv_frame_segment(s)

        assert self.frame_assembler.get_latest_frame() == output

    def test_frame_assembler(self):
        self.assert_segments_produce([
            FrameSegment(1, 0, b'pa', False),
            FrameSegment(1, 1, b'ylo', False),
            FrameSegment(1, 2, b'ad', True),
        ], b'payload')


    def test_frame_assembler_2(self):
        self.assert_segments_produce([
            FrameSegment(1, 0, b'gar', False),
            FrameSegment(1, 1, b'bage', True),
            FrameSegment(2, 0, b'pay', False),
            FrameSegment(2, 1, b'load', True),
        ], b'payload')

    def test_frame_assembler__intertwined_output(self):
        self.assert_segments_produce([
            FrameSegment(1, 0, b'gar', False),
            FrameSegment(2, 0, b'pay', False),
            FrameSegment(1, 1, b'bage', False),
            FrameSegment(2, 1, b'load', True),
        ], b'payload')

    def test_frame_assembler__frames_out_of_order(self):
        self.assert_segments_produce([
            FrameSegment(1, 0, b'gar', False),
            FrameSegment(2, 0, b'pay', False),
            FrameSegment(2, 1, b'load', True),
            FrameSegment(1, 1, b'bage', True),
        ], b'payload')
