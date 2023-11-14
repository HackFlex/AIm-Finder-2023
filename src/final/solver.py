from xmlHandler import xmlHandler
from TextProcessor import TextProcessor, LoRALayer
from outputNNHandler import outNNHandler
import json

class solver:
    def __init__(self):
        self.processor = TextProcessor()
        pass
        
    def solve(self, pathXml, taskId):
        xml = xmlHandler(pathXml)
        sections = xml.getSections()
        tokenizeText = xml.getTokenizeText()
        ###NN
        arrDict = self.processor.process_texts(tokenizeText)
        ###out NN to valid dict
        handler = outNNHandler()
        jsonDict = []
        for i in range(len(arrDict)):
            arr = handler.generateJsonSection(sections[i], arrDict[i])
            for symptom in arr:
                jsonDict.append(symptom)
        ###save to file
        pathJsonHost = "/".join(pathXml.split("/")[:-2]) + "/output/" + str(taskId) + "_1_" + str(taskId) + ".json"
        with open(pathJsonHost, 'w') as fp:
            json.dump(jsonDict, fp)
        pathJsonContainer =   "/app/" + "/".join(pathJsonHost.split("/")[-5:])
        ###send Json
        handler.sendJson(pathJsonContainer, taskId)

if __name__ == '__main__':
    s = solver()
    s.solve("/home/ilya/School/baseline/files/sessions/895/input/8595_1_8595.xml", 1234)
    s.solve("/home/ilya/School/baseline/files/sessions/895/input/8576_1_8576.xml", 12345)
    s.solve("/home/ilya/School/baseline/files/sessions/895/input/8532_1_8532.xml", 12346)
