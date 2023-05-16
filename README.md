# Video Backup Utility

This utility allows for encoding and decoding of arbitrary files as MP4 videos. One potential use is to create TAR archives and upload them to YouTube.

## Encoding

```
$ tar cvfz out.tgz source_dir/*           # Create an zipped archive.
$ python3 encoder.py out.tgz out.tgz.mp4  # Encode as video.
# Upload to YouTube or elsewhere.
```

## Decoding

```
# Download from YouTube using https://wave.video/convert/youtube-to-mp4-130.
$ python3 decoder.py out.tgz.mp4 out-recovered.tgz
$ tar xzf out-recovered.tgz
```