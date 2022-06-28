import sys
sys.path.append("/mnt/python3/dog-cat-lib")
import train

def handler(event, context):
    train.strengthen()
    return "Hello world"