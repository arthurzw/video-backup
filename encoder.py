from constants import *
import numpy as np
import moviepy.editor as mpy
import sys

def read_file_to_bytes(file_path):
    with open(file_path, "rb") as file:
        byte_array = bytearray(file.read())
    return byte_array

def set_pixel(surface, x, y, color):
    surface[x * DX:(x + 1) * DX, y * DY:(y + 1) * DY] = color

def render_frame(surface, data, offset):
    length = len(data)
    for y in range(CY):
        for x in range(CX):
            i = offset + CX * y + x
            if i < length:
                b = data[i]
                assert b < 256
                set_pixel(surface, y, x, BYTE_COLORS[b])
            else:
                set_pixel(surface, y, x, (0, 0, 0))

def generate_frames(data):
    length = len(data)
    def gen(t):
        offset = int(t * FPS) * BYTES_PER_FRAME
        surface = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        render_frame(surface, data, offset)
        return surface
    return gen

def encode(filename, data):
    gen = generate_frames(data)
    num_frames = len(data) // BYTES_PER_FRAME + 1
    print(f'Encoding {len(data)} bytes into {num_frames} frames...')
    clip = mpy.VideoClip(make_frame=generate_frames(data), duration=num_frames/FPS)
    clip.write_videofile(filename, fps=FPS)
    clip.close()

if len(sys.argv) > 2:
    input = sys.argv[1]
    output = sys.argv[2]
    data = read_file_to_bytes(sys.argv[1])
    encode(output, data)
else:
    print(f"Usage: {sys.argv[0]} <input> <output>")