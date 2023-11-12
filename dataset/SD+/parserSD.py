from os import listdir
from os.path import isfile, join
import json

def getNameFiles(folderPath):
    onlyfiles = [f for f in listdir(folderPath) if isfile(join(folderPath, f))]
    return onlyfiles

def getDict(path, symptom):
    with open(path) as f:
        dict = {"tokens": [], "ner_tags": []}
        lines = f.readlines()
        for line in lines:
            line = line.replace("\t", " ")
            line = line.replace("\n", "")
            tokens = line.split(" ")
            ner_tags = []
            for i in range(len(tokens)):
                if symptom == True:
                    ner_tags.append(int(i > 0) + 1)
                else:
                    ner_tags.append(0)
            dict['tokens'].append(tokens)
            dict['ner_tags'].append(ner_tags)
    return dict

if __name__ == '__main__':
    
    symptomDict = {"tokens": [], "ner_tags": []}
    noSymptomDict = {"tokens": [], "ner_tags": []}
    
    folder = "Symptoms"
    nameFiles = getNameFiles(folder)
    for file in nameFiles:
        tmp = getDict(f'{folder}/{file}', True)
        symptomDict['tokens'].extend(tmp['tokens'])
        symptomDict['ner_tags'].extend(tmp['ner_tags'])

    folder = "NotSymptoms"
    nameFiles = getNameFiles(folder)
    for file in nameFiles:
        tmp = getDict(f'{folder}/{file}', False)
        noSymptomDict['tokens'].extend(tmp['tokens'])
        noSymptomDict['ner_tags'].extend(tmp['ner_tags'])
        
    resultDict = {"tokens": [], "ner_tags": []}
    
    resultDict['tokens'].extend(symptomDict['tokens'])
    resultDict['ner_tags'].extend(symptomDict['ner_tags'])
    
    resultDict['tokens'].extend(noSymptomDict['tokens'])
    resultDict['ner_tags'].extend(noSymptomDict['ner_tags'])
    
    with open("datasetSD.json", "w", encoding='utf-8') as fp:
        json.dump([resultDict] , fp, ensure_ascii=False)
        print(len(resultDict['ner_tags']), len(resultDict['tokens']))
    
    with open("symptomDict.json", "w", encoding='utf-8') as fp:
        json.dump([symptomDict] , fp, ensure_ascii=False)
        print(len(symptomDict['ner_tags']), len(symptomDict['tokens']))
    
    with open("noSymptomDict.json", "w", encoding='utf-8') as fp:
        json.dump([noSymptomDict] , fp, ensure_ascii=False)
        print(len(noSymptomDict['ner_tags']), len(noSymptomDict['tokens']))
