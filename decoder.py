from constants import *
import numpy as np
import moviepy.editor as mpy
import sys
import binascii

def decode_byte(color):
    c = np.array(color)
    distances = np.linalg.norm(BYTE_COLORS_NP - c, axis=1)
    return np.argmin(distances)

def decode_frame(image):
    frame_id = 0
    frame_id_bytes = 8
    data = []
    for y in range(CY):
        for x in range(CX):
            square = image[y * DY:(y + 1) * DY, x * DX:(x + 1) * DX, :]
            color = tuple(np.uint8(np.mean(square, axis=(0, 1))))
            byte = decode_byte(color)
            if byte == 256:
                break
            if frame_id_bytes > 0:
                frame_id <<= 8
                frame_id |= byte
                frame_id_bytes -= 1
            else:
                data.append(np.uint8(byte))
    print(f"Decoded frame ID {frame_id}")
    return (frame_id, data)

# Decodes the file and invokes the callback for each buffer read from the file.
def decode(filename, callback):
    video = mpy.VideoFileClip(filename)
    prev_frame_id = -1
    for frame in video.iter_frames():
        frame_id, data = decode_frame(np.array(frame))
        if frame_id != prev_frame_id:
            prev_frame_id = frame_id
            callback(data)

if len(sys.argv) > 2:
    input = sys.argv[1]
    output = sys.argv[2]
    with open(output, "wb") as file:
        decode(input, lambda data: file.write(bytes(data)))
else:
    print(f"Usage: {sys.argv[0]} <input> <output>")
