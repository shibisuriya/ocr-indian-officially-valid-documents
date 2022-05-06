import json
import boto3
import base64
import re


from drivingLicenseFront import drivingLicenseFront
from pan import pan
from complexPan import complexPan
from aadhaarFront import aadhaarFront
from aadhaarBack import aadhaarBack
from panClassifier import panClassifier
from aadhaarClassifier import aadhaarClassifier


def lambda_handler(event, context):
    client = boto3.client('textract')
    base64image = json.loads(event['body'])['base64image'].split('base64,')[1]
    binaryImage = bytearray(base64.b64decode(base64image))
    data = client.detect_document_text(
        Document = {
            'Bytes': binaryImage
        }
    )
    # response['image'] = json.loads(event['body'])['base64image']
    if(data['DocumentMetadata']['Pages'] > 1):
        return {
            'statusCode': 428,
            'body': 'Multiple pages found in the document uploaded...'
        }
    else:
        data = data['Blocks']
        ocrData = {}
        for line in data:
               if(line['BlockType'] == 'LINE'):
                    text = line['Text'].strip()
                    # Driving license... 
                    if(bool(re.search('(([A-Z]{2}[0-9]{2})( )|([A-Z]{2}-[0-9]{2}))((19|20)[0-9][0-9])[0-9]{7}$', text))):
                        ocrData = drivingLicenseFront(data)
                        break
                        
                    # PAN    
                    if(bool(re.match('[A-Z]{5}[0-9]{4}[A-Z]{1}', text))):
                        ocrData = panClassifier(data)
                        break
                        
                    # Aadhaar 
                    if(bool(re.match('[0-9]{4} [0-9]{4} [0-9]{4}$', text))):
                        ocrData = aadhaarClassifier(data)
                        break
    resp = {}
    resp['base64image'] = json.loads(event['body'])['base64image']
    resp['ocrData'] = ocrData
    resp['rawData'] = data
    return {
            'statusCode': 200,
            'body': json.dumps(resp)
    }

