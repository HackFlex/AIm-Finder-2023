from lxml import etree, objectify
import json


def get_xpath(tree, search_text, answer) -> None:
    root = tree.getroot()
    ns = root.nsmap
    lst = tree.xpath(f'//*[contains(text(), "{search_text}")]')
    item = lst[0]
    # print(item.getparent())
    prefix = '/' + root.tag + '/'
    path = tree.getelementpath(item.getparent())    
    full_path = (prefix + path).replace('{' + ns[None] + '}', '')
    res = tree.findall(path)
    
    for element in item.getparent().iter(tag='{' + ns[None] + '}text'):
        if (item.getparent() == element.getparent()):
            # print(element.text)
            # print(len(element.text))
            anamnesis = element.text.strip()
            break
        # if (element.tag == '{urn:hl7-org:v3}text'):
        # print("%s - %s" % (element.tag, element.text))
        # print(element.getparent())
            # break
    
    # print(item.getparent().findall("./*", namespaces=ns))
    
    # print(path)
    # print(res)

    
    # return full_path
    answer[0]['xPath'] = full_path
    answer[0]['name'] = anamnesis
    answer[0]['end'] = len(anamnesis) 


answer = [{
    'xPath': '',
    'start': 0,
    'end': 0,
    'name': '',
    'decorCode': 'anamnesis',
    'code': ''
}]


if __name__ == '__main__':

    input_file = './oldsessions/test.xml'
    search_text = 'АНАМНЕЗ'
    
    tree = etree.parse(input_file)
    
    get_xpath(tree, search_text, answer)
    
    print(answer)

    with open('output.json', 'w') as f:
        json.dump(answer, f, indent=4, ensure_ascii=False)