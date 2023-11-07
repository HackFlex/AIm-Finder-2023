from xmlHandler import xmlHandler
from NN import NN

import pickle
import outputNNHandler as out
import json

class solver:
    def __init__(self):
        pass
        
    def solve(self, pathXml, taskId, tmp_result_path=None):
        xml = xmlHandler(pathXml)
        sections = xml.getSections() # [ { 'xPath': "", 'text': "" } ]
        
        
        print("----")
        for s in sections:
            for item in s:
                print('\033[95m' + item['xPath'] + '\033[0m')
                print()
                print(item['name'])
                print("----")
            
        tokenizeText = xml.getTokenizeText()
        print('\033[95m' + 'Tokenize Text' + '\033[0m')
        print(tokenizeText)
        print("----")
        print(NN().searchSymptoms(tokenizeText))
        
        ##processingOutputNN and generate json
        ##send json

        print('===OUTPUT===')

        result = None
        if tmp_result_path:
            with open(tmp_result_path, "rb") as file:
                result = pickle.load(file)

        print(json.dumps(result, indent=4, ensure_ascii=False))
        # print()
        # print(json.dumps(sections, indent=4))
        
        result_data = []
        # for i in range(len(sections)):
        for item in sections[0]:
            data = out.tmp(item['name'], result[0])
            if data:
                result_data.append(data)
        print(result_data)

if __name__ == '__main__':
    s = solver()
    s.solve("/home/maksim/CONTESTS/aim-finder/AIm-Finder-2023/src/final/test1.xml", "10011",
            tmp_result_path='/home/maksim/CONTESTS/aim-finder/nn-results/res0.pickle')
    # s.solve("/home/ilya/School/baseline/MedFlexSolve/src/final/test2.xml", "10011",
            # tmp_result_path='/home/maksim/CONTESTS/aim-finder/nn-results/res1.pickle')
    # s.solve("/home/ilya/School/baseline/MedFlexSolve/src/final/Эпикриз_1241413117_v1.xml", "10011",
            # tmp_result_path='/home/maksim/CONTESTS/aim-finder/nn-results/res2.pickle')
    