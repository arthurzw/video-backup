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
    data = []
    for y in range(CY):
        for x in range(CX):
            square = image[y * DY:(y + 1) * DY, x * DX:(x + 1) * DX, :]
            color = tuple(np.uint8(np.mean(square, axis=(0, 1))))
            byte = decode_byte(color)
            if byte == 256:
                break
            data.append(np.uint8(byte))
    return data

# Decodes the file and invokes the callback for each buffer read from the file.
def decode(filename, callback):
    video = mpy.VideoFileClip(filename)
    checksum = 0
    for frame in video.iter_frames():
        data = decode_frame(np.array(frame))
        new_checksum = binascii.crc32(bytes(data))
        if new_checksum != checksum:
            checksum = new_checksum
            callback(data)

if len(sys.argv) > 2:
    input = sys.argv[1]
    output = sys.argv[2]
    with open(output, "wb") as file:
        decode(input, lambda data: file.write(bytes(data)))
else:
    print(f"Usage: {sys.argv[0]} <input> <output>")
