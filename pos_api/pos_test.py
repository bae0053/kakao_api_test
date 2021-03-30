import requests

APP_KEY = 'YOUR KEY'
IMAGE_URL = 'http://topclass.chosun.com/news_img/1802/1802_008.jpg'
IMAGE_FILE_PATH = 'example.jpg'
session = requests.Session()
session.headers.update({'Authorization': 'KakaoAK ' + APP_KEY})

# URL로 이미지 입력시
response = session.post('https://cv-api.kakaobrain.com/pose', data={'image_url': IMAGE_URL})
print(response.status_code, response.json())

# 파일로 이미지 입력시
# with open(IMAGE_FILE_PATH, 'rb') as f:
#     response = session.post('https://cv-api.kakaobrain.com/pose', files=[('file', f)])
#     print(response.status_code, response.json())
