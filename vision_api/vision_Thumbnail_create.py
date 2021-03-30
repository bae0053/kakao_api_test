import sys
import argparse
import requests
from PIL import Image, ImageFilter

API_URL = 'https://dapi.kakao.com/v2/vision/thumbnail/detect'
MYAPP_KEY = 'MY_KEY'
# 해당 이미지에서 주요 부분을 선택해 썸네일로 보여주는 예제


def detect_thumbnail(filename, width, height):
    headers = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}

    try:
        files = { 'image' : open(filename, 'rb')}
        params = {'width': width, 'height': height}
        resp = requests.post(API_URL, headers=headers, data=params, files=files)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(str(e))
        sys.exit(0)

def show_thumbnail(filename, detection_result, width, height):
    image = Image.open(filename)
    rect = detection_result['result']['thumbnail']
    thumbnail = image.crop((rect['x'], rect['y'], rect['x'] + rect['width'], rect['y'] + rect['height']))
    thumbnail = thumbnail.resize((width, height))

    return thumbnail


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Make a thumbnail.')
    parser.add_argument('image_file', type=str, nargs='?', default="./uinna.jpg",
                        help='image file to make a thumbnail')
    parser.add_argument('width', type=int, nargs='?', default=150,
                        help='thumbnail width')
    parser.add_argument('height', type=int, nargs='?', default=200,
                        help='thumbnail height')

    args = parser.parse_args()

    detection_result = detect_thumbnail(args.image_file, args.width, args.height)
    image = show_thumbnail(args.image_file, detection_result, args.width, args.height)
    image.show()
