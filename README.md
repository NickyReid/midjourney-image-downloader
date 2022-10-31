# midjourney-image-downloader
Download your Midjourney gallery.

Copied from https://github.com/timmc/midjourney-history-sync ⭐ and adapted with additional advice from [timmc](https://github.com/timmc) ️

## About
- Only saves Upscaled images
- Saves images in date folders with prompt as filename, eg:
```/midjourney-image-downloader/jobs/2022/10/23/057b9a3b-1f2b-4279-9d27-63a102cbed79/prompt.png```
- Safe to stop and resume
- If you don't have more than 5000 total upscaled images, this script should be able to download all of them.
- Midjourney API paging is limited to 50

## To run
Install:
 ```pip install -e .```

Run:
```python download.py```

