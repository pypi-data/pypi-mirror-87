# mhyt


mhyt is a Python library for
download movies and music from youtube

mhyt can run in python 3+

## examples
```python
from mhyt import yt_download
url = "https://www.youtube.com/watch?v=0BVqFYParRs"
file = "Clouds.mp4"
yt_download(url,file)
#########################
file = "Clouds_music.mp3"
yt_download(url,file,ismusic=True)
```
### Installing
To install with pip:
```
(sudo) pip install mhyt
```

## Built With
* [youtube_dl](https://github.com/ytdl-org/youtube-dl) - to download files from youtube
* [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg) - to download ffmpeg 
## Author
**matan h**
## License
This project is licensed under the MIT License.

