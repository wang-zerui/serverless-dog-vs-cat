import sys
sys.path.append("/mnt/python3/dog-cat-lib")
import bottle
import base64
import json
import random
from train import strengthen
import os
cacheDir = '/mnt/python3/strength/'
randomStr = lambda num=5: "".join(random.sample('abcdefghijklmnopqrstuvwxyz', num))

def save_image(data):
    image = data.get("image")
    label = data.get("label")
    localName = label + randomStr(10) + ".jpg"
    imagePath = cacheDir + localName

    with open(imagePath, 'wb') as f:
        f.write(base64.b64decode(image))
    return imagePath

@bottle.route('/upload', method='POST')
def getComicStyle():
    result = {}
    postData = json.loads(bottle.request.body.read().decode("utf-8"))
    
    save_image(postData)
    TRAIN_PATH = "/mnt/python3/strength"
    # 如果文件数大于100就强化模型
    filenames = os.listdir(TRAIN_PATH)
    if len(filenames) > 100:
        strengthen(TRAIN_PATH)
        for i in filenames:
            c_path = os.path.join(TRAIN_PATH, i)
            if os.path.isdir(c_path):
                pass
            else:
                os.remove(c_path)
    return {"code": 0}

app = bottle.default_app()

if __name__ == "__main__":
    bottle.run(host='localhost', port=8099)