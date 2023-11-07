from xmlHandler import xmlHandler
from NN import NN

class solver:
    def __init__(self):
        pass
        
    def solve(self, pathXml, taskId):
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

if __name__ == '__main__':
    s = solver()
    s.solve("/home/ilya/School/baseline/MedFlexSolve/src/final/test1.xml", "10011")
    s.solve("/home/ilya/School/baseline/MedFlexSolve/src/final/test2.xml", "10011")
    s.solve("/home/ilya/School/baseline/MedFlexSolve/src/final/Эпикриз_1241413117_v1.xml", "10011")
    