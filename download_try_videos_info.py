from __future__ import unicode_literals
import youtube_dl

import requests

from PIL import Image


def crop_image_black(image):
    _image = Image.open(image)
    black = (0, 0, 0)
    #
    for h in xrange(_image.height):
        if _image.getpixel((10, h)) != black:
            top = h
            break
    for h in xrange(_image.height-1, 0, -1):
        if _image.getpixel((10, h)) != black:
            bottom = h
            break
    size = (0, top, _image.width, bottom)
    _image.crop(size).save(image)
    return None


def download_img(video_id):
    filename = "".join([video_id, ".jpg"])
    url = "https://i.ytimg.com/vi/{}/sddefault.jpg".format(video_id)
    res = requests.get(url)
    with open(filename, "wb") as f:
        for chunk in res.iter_content(1024):
            f.write(chunk)
    return None


def download_video(video_id):
    ydl_opts = {
                   'outtmpl': "%(id)s.%(ext)s"
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(['http://www.youtube.com/watch?v={}'.format(video_id)])

if __name__ == '__main__':
    import os
    from youtube import get_uploads_list_id, get_playlist_items
    from transcript import get_clean_transcript, download_transcript

    os.chdir('./static/try_resource')
    # Seeker
    channel_id = 'UCzWQYUVCpZqtN93H8RR44Qw'
    upload_list_id = get_uploads_list_id(channel_id)
    video_ids = get_playlist_items(upload_list_id)
    counter = 0
    for video_id in video_ids:
        if counter > 25:
            break
        _transcript = download_transcript(video_id)
        if _transcript == '':
            continue
        else:
            with open("".join([video_id, '.txt'])) as f:
                f.write(get_clean_transcript(_transcript))
            download_img(video_id)
            crop_image_black(video_id)
            download_video(video_id)
            counter += 1



