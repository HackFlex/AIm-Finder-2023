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
            'code': ''
        }

    def __searchSingleSection(self, nameSection):
        tree = etree.parse(self.pathXml)

        root = tree.getroot()
        ns = root.nsmap
        lst = tree.xpath(f'//*[contains(text(), "{nameSection}")]')
        answer_list = []
        
        for item in lst:
            # print(item.getparent())
            prefix = '/' + root.tag + '/'
            path = tree.getelementpath(item.getparent())    
            full_path = (prefix + path).replace('{' + ns[None] + '}', '')
            # full_path = change_array_indexes(full_path, -1)
            anamnesis = ''
            for element in item.getparent().iter(tag='{' + ns[None] + '}text'):
                if (item.getparent() == element.getparent()):
                    anamnesis = element.text.strip()
                    break
                # if (element.tag == '{urn:hl7-org:v3}text'):
                # print("%s - %s" % (element.tag, element.text))
                # print(element.getparent())
                    # break
            
            answer = self.__get_answer_object()
            answer['xPath'] = full_path + '/text'
            answer['name'] = anamnesis
            answer['end'] = len(anamnesis)

            answer_list.append(answer)
        
        return answer_list
        
    def __searchSections(self):
        sections = []
        for name in self.searchHeaderNames:
            sections.append(self.__searchSingleSection(name))
        return sections
    
    def __tokenizeText(self):
        retArray = []
        sections = self.getSections()
        for s in sections:
            for item in s:
                retArray.append(item['name'].split(' '))
        
        return (retArray)
        
    def getSections(self):
        return self.sections
    
    def getTokenizeText(self):
        return self.tokenizeText