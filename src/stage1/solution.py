from lxml import etree
import json

def get_answer_object() -> dict:
    return {
        'xPath': '',
        'start': 0,
        'end': 0,
        'name': '',
        'decorCode': 'anamnesis',
        'code': ''
    }


def change_array_indexes(path: str, value: int) -> str:
    start, end = 0, 0
    start = path.find('[')
    end = path.find(']')

    while start != -1:
        try:
            num = int(path[start+1:end]) + value
            path = path[:start+1] + str(num) + path[end:]
        except ValueError:
            pass
        start = path.find('[', end)
        end = path.find(']', start)

    return path


def solve(input_file, search_text) -> None:
    tree = etree.parse(input_file)

    root = tree.getroot()
    ns = root.nsmap
    lst = tree.xpath(f'//*[contains(text(), "{search_text}")]')
    answer_list = []

    for item in lst:
        # print(item.getparent())
        prefix = '/' + root.tag + '/'
        path = tree.getelementpath(item.getparent())    
        full_path = (prefix + path).replace('{' + ns[None] + '}', '')
        # full_path = change_array_indexes(full_path, -1)
        
        for element in item.getparent().iter(tag='{' + ns[None] + '}text'):
            if (item.getparent() == element.getparent()):
                anamnesis = element.text.strip()
                break
            # if (element.tag == '{urn:hl7-org:v3}text'):
            # print("%s - %s" % (element.tag, element.text))
            # print(element.getparent())
                # break
        
        answer = get_answer_object()
        answer['xPath'] = full_path + '/text'
        answer['name'] = anamnesis
        answer['end'] = len(anamnesis)

        answer_list.append(answer)

    return answer_list


if __name__ == '__main__':

    input_file = './oldsessions/test.xml'
    search_text = 'АНАМНЕЗ'
    
    answer = solve(input_file, search_text)
    
    print(answer)

    with open('output.json', 'w') as f:
        json.dump(answer, f, indent=4, ensure_ascii=False)