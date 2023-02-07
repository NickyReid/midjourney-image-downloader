# midjourney-image-downloader
Download your Midjourney gallery and all images

forked from [NickyReid/midjourney-image-downloader](https://github.com/NickyReid/midjourney-image-downloader) ️

## About
- Default: saves images in date folders with prompt as filename, eg:
```/midjourney-image-downloader/jobs/2022/10/23/057b9a3b-1f2b-4279-9d27-63a102cbed79/prompt.png``` (Can be disabled: ```USE_DATE_FOLDERS```)
- Default: only saves upscaled images (Can be changed: ```UPSCALES_ONLY```/```GRIDS_ONLY```)
- Safe to stop and resume
- Midjourney API caps paging at 50. This script pages to 50 using all known "orderBy" options to try and get a complete sync with the web gallery. If you have less than 5001 images then you should be able to get a full sync using this script. 
- OUTPUT_FOLDER : choose where to save your images

## To run
Install:
 ```pip install -e .```

Run:
```python download.py```

