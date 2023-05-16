import numpy as np

WIDTH = 1280
HEIGHT = 720
DX = 16
DY = 16
CX = WIDTH // DX
CY = HEIGHT // DY
# G is compressed the least, so use it more than R/B channels. We try to encode 1 byte per pixel.
COLOR_VALUES_8 = [3 + n * 36 for n in range(8)]  # 3 is added to further differentiate used colors from (0, 0, 0) meaning no data.
COLOR_VALUES_6 = [n * 51 for n in range(6)]
BYTE_COLORS = [(r, g, b) for r in COLOR_VALUES_6 for g in COLOR_VALUES_8 for b in COLOR_VALUES_6][1:257]  # (0, 0, 0) is used for no data.
BYTE_COLORS_NP = np.array(BYTE_COLORS + [(0, 0, 0)])
FRAME_HEADER_LEN = 8
BYTES_PER_FRAME = CX * CY - FRAME_HEADER_LEN
FPS = 4