import sys
sys.path.append("/mnt/python3/dog-cat-lib")
import bottle
import base64
import json
import random
from predict import predict


cacheDir = '/tmp/'
randomStr = lambda num=5: "".join(random.sample('abcdefghijklmnopqrstuvwxyz', num))

def save_image(data):
    image = data.get("image")
    localName = randomStr(10) + ".jpg"
    imagePath = cacheDir + localName

    with open(imagePath, 'wb') as f:
        f.write(base64.b64decode(image))
    return imagePath

@bottle.route('/dog-vs-cat', method='POST')
def getComicStyle():
    result = {}
    postData = json.loads(bottle.request.body.read().decode("utf-8"))

    imagePath = save_image(postData)

    result = predict(imagePath)
    result['code'] = "0"
    print(result)
    return result

@bottle.route('/test', method='POST')
def getComicStyle():
    return {"dog": 0.97, "cat": 0.03}
app = bottle.default_app()

if __name__ == "__main__":
    bottle.run(host='localhost', port=8099)