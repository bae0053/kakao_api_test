import cv2
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from pycocotools.coco import COCO
from requests import Session

APP_KEY = 'YOUR KEY'
APP_KEY = '319e0bb3ea0234a4d3d914dbacbf5c84'
session = Session()
session.headers.update({'Authorization': 'KakaoAK ' + APP_KEY})


def inference(filename):
    with open(filename, 'rb') as f:
        response = session.post('https://cv-api.kakaobrain.com/pose', files={'file': f})
        response.raise_for_status()
        return response.json()


def visualize(filename, annotations, threshold=0.2):
    # 낮은 신뢰도를 가진 keypoint들은 무시
    for annotation in annotations:
        keypoints = np.asarray(annotation['keypoints']).reshape(-1, 3)
        low_confidence = keypoints[:, -1] < threshold
        keypoints[low_confidence, :] = [0, 0, 0]
        annotation['keypoints'] = keypoints.reshape(-1).tolist()

    # COCO API를 활용한 시각화
    image = cv2.cvtColor(cv2.imread(filename, cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.axis('off')
    coco = COCO()
    coco.dataset = {
        "categories": [
            {
                "supercategory": "person",
                "id": 1,
                "name": "person",
                "keypoints": ["nose", "left_eye", "right_eye", "left_ear", "right_ear", "left_shoulder",
                              "right_shoulder", "left_elbow", "right_elbow", "left_wrist", "right_wrist", "left_hip",
                              "right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle"],
                "skeleton": [[1, 2], [1, 3], [2, 3], [2, 4], [3, 5], [4, 6], [5, 7], [6, 7], [6, 8], [6, 12], [7, 9],
                             [7, 13], [8, 10], [9, 11], [12, 13], [14, 12], [15, 13], [16, 14], [17, 15]]
            }
        ]
    }
    coco.createIndex()
    coco.showAnns(annotations)
    plt.show()


IMAGE_FILE_PATH = './son.jpg'
result = inference(IMAGE_FILE_PATH)
visualize(IMAGE_FILE_PATH, result)