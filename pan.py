import re
def pan(data):
    ocrData = {}
    lines = []
    for line in data:
           if(line['BlockType'] == 'LINE'):
                text = line['Text'].strip()
                # We have to get rid of the 'Text' with lowercase (all lowercase), simple PAN card doesn't have any useful 
                # information written on it in lowercase.
                # All letters should be in lower case, then this condition will skip that word.
                if(text.islower() == False):
                    lines.append(line['Text'])
    for index, text in enumerate(lines):
            # Pattern matching for DOB.
            if(bool(re.match('\d{2}/\d{2}/\d{4}', text))):
                ocrData['dob'] = text
            # Pattern matching for PAN.
            if(bool(re.match('[A-Z]{5}[0-9]{4}[A-Z]{1}', text))):
                ocrData['pan'] = text
            if(text == 'GOVT. OF INDIA'):
                # The line after 'GOVT. OF INDIA' in all PAN card is the name of the person.
                ocrData['name'] = lines[index + 1]
                # The line after the name of the person is his father's name, sometimes hindi words from the logo and hologram
                # gets read as some garbage english words (they are in lowercase and we have got rid of them in the previous step
                # itself).
                ocrData['fatherName'] = lines[index + 2]
    ocrData['type'] = 'simplePan'
    return ocrData
