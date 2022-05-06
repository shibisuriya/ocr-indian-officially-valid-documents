from complexPan import complexPan
from pan import pan
def panClassifier(data):
    ocrData = {}
    for line in data:
        if(line['BlockType'] == 'LINE'):
            text = line['Text'].strip()
            if("father's" in text.lower()):
                return complexPan(data)
    return pan(data)
