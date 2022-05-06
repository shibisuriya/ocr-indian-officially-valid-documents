import re
def aadhaarBack(data):
    ocrData = {}
    addressLeft = 0
    address = ''
    for object in data:
        if(object['BlockType'] == 'LINE'):
            line = object['Text']
            if(bool(re.search('Address', line))):
                addressLeft = object['Geometry']['BoundingBox']['Left']
                break
    imperfection = 3 / 100
    min_x = addressLeft - imperfection * addressLeft 
    max_x = addressLeft +  imperfection * addressLeft
    for object in data:
        if(object['BlockType'] == 'LINE'):
            text = object['Text']
            
            # To extract Aadhaar number... 
            if(bool(re.match('[0-9]{4} [0-9]{4} [0-9]{4}$', text))):
                ocrData['aadhaar'] = text
                
            # To extract address... 
            left = object['Geometry']['BoundingBox']['Left']
            if(left > min_x and left < max_x):
                    address = address + text
    ocrData['address'] = address
    return ocrData
