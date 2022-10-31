# midjourney-image-downloader
Download images from your Midjourney web gallery.

Copied from https://github.com/timmc/midjourney-history-sync ⭐️

## About
- Only saves Upscaled images
- Saves images in date folders with prompt as filename, eg:
/midjourney-image-downloader/jobs/2022/10/23/057b9a3b-1f2b-4279-9d27-63a102cbed79/prompt.png
- Safe to stop and resume
- If you don't have more than 5000 total upscaled images, this script should be able to download all of them.
- Midjourney API paging is limited to 50

## To run
Install:
 ```pip install -e .```

Run:
```python download.py```

