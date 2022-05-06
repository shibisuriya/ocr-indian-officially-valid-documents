import re
def complexPan(data):
    ocrData = {}
    lines = []
    for line in data:
           if(line['BlockType'] == 'LINE'):
                text = line['Text'].strip()
                lines.append(text)
    for index, text in enumerate(lines):
            print(index, ') ', text)
            # Pattern matching for DOB.
            if(bool(re.match('\d{2}/\d{2}/\d{4}', text))):
                ocrData['dob'] = text
            # Pattern matching for PAN.
            if(bool(re.match('[A-Z]{5}[0-9]{4}[A-Z]{1}', text))):
                ocrData['pan'] = text
            if('name' in text.lower()):
                if('father' in text.lower()):
                    ocrData['fatherName'] = lines[index + 1]
                else:
                    ocrData['name'] = lines[index + 1]
    ocrData['type'] = 'complexPan'
    return ocrData
