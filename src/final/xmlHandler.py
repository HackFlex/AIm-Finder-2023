from lxml import etree
import json

class xmlHandler:
    def __init__(self, pathXml):
        self.pathXml = pathXml
        self.searchHeaderNames = [
            'Анамнез заболевания',
            'ОБЪЕКТИВИЗИРОВАННАЯ ОЦЕНКА СОСТОЯНИЯ БОЛЬНОГО',
            'ФИЗИКАЛЬНЫЕ ПАРАМЕТРЫ',
            'ФИЗИКАЛЬНОЕ ОБСЛЕДОВАНИЕ'
            ]
        self.sections = self.__searchSections()
        self.tokenizeText = self.__tokenizeText()
        
    def __get_answer_object(self) -> dict:
        return {
            'xPath': '',
            'start': 0,
            'end': 0,
            'name': '',
            'decorCode': 'symptom',
            'code': '',
            'nameSection': ''
        }

    def __searchSingleSection(self, nameSection):
        tree = etree.parse(self.pathXml)

        root = tree.getroot()
        ns = root.nsmap
        lst = tree.xpath(f'//*[contains(text(), "{nameSection}")]')
        answer_list = []
        textInParagraph = False
        for item in lst:
            # print(item.getparent())
            prefix = '/' + root.tag + '/'
            path = tree.getelementpath(item.getparent())    
            full_path = (prefix + path).replace('{' + ns[None] + '}', '')  + '/text'
            # full_path = change_array_indexes(full_path, -1)
            anamnesis = ''
            for element in item.getparent().iter(tag='{' + ns[None] + '}text'):
                if (item.getparent() == element.getparent()):
                    anamnesis = element.text.strip()
                    if (anamnesis == ""):
                        textInParagraph = True
                        break
            if(textInParagraph == True):
                i = 0
                for element in item.getparent().iter(tag='{' + ns[None] + '}paragraph'):
                    i += 1
                    anamnesis = element.text.strip()
                    answer = self.__get_answer_object()
                    answer['xPath'] = full_path + f'/paragraph[{i}]'
                    answer['name'] = anamnesis
                    answer['end'] = len(anamnesis)
                    answer['nameSection'] = nameSection

                    answer_list.append(answer)
            else:
                answer = self.__get_answer_object()
                answer['xPath'] = full_path
                answer['name'] = anamnesis
                answer['end'] = len(anamnesis)
                answer['nameSection'] = nameSection

                answer_list.append(answer)
        return answer_list
        
    def __searchSections(self):
        sections = []
        for name in self.searchHeaderNames:
            singleSection = self.__searchSingleSection(name)
            for s in singleSection:
                sections.append(s)
        return sections
    
    def __tokenizeText(self):
        retArray = []
        sections = self.getSections()
        for item in sections:
            retArray.append(item['name'].split(' '))    
        return (retArray)
        
    def getSections(self):
        return self.sections
    
    def getTokenizeText(self):
        return self.tokenizeText

def parseSingleXml(xmlPath):
    handler = xmlHandler(xmlPath)
    sections = handler.getSections()
    
    print()
    print('\033[95m' + xmlPath + '\033[0m')
    print("----")
    for item in sections:
        print('\033[95m' + item['nameSection'] + '\033[0m')
        print(item['xPath'])
        print()
        print(item['name'])
        print("----")

if __name__ == '__main__':
    parseSingleXml("/home/ilya/School/baseline/files/sessions/895/input/8595_1_8595.xml")
    # parseSingleXml("/home/ilya/School/baseline/files/sessions/895/input/8576_1_8576.xml")
    # parseSingleXml("/home/ilya/School/baseline/files/sessions/895/input/8532_1_8532.xml")
    