import shlex
import subprocess

class outNNHandler:
    def __init__(self):
        pass

    def _getSymptomJson(self, xPath, start, end, name) -> dict:
        return {
            'xPath': xPath,
            'start': start,
            'end': end,
            'name': name,
            'decorCode': 'symptom',
            'code': ''
        }

    def sendJson(self, pathJson, taskId):
        cmd = f'docker exec -it baseline sh -c "python baseline.py send --path={pathJson} --taskid={taskId}" > ./log.txt'
        cmds = shlex.split(cmd)
        process = subprocess.run(cmds, start_new_session=True)

    def generateJsonSection(self, srcSection, outSection):
        arrSymptoms = []
        # print(srcSection['name'])

        for symptom in outSection['symptoms']:

            start_nn, end_nn = [int(item) for item in symptom]
            text_nn = outSection['text'][start_nn:end_nn]
            result = self.__get_real_bounds_and_text(
                srcSection['name'], text_nn, start_nn, end_nn)
            if result is None:
                continue
            start_base, end_base, text_symptom = result

            symptomJson = self._getSymptomJson(
                srcSection['xPath'],
                start_base,
                end_base,
                text_symptom)
            arrSymptoms.append(symptomJson)
        return arrSymptoms
    
    def __get_real_bounds_and_text(self, text_base: str, text_nn: str,
                                   start_nn: int, end_nn: int):
        # print(f'start={start_nn} end={end_nn} text="{text_nn}"', end=' | ')
        
        # Выберем точку старта в основном тексте для поиска симптома
        index = text_base.rfind(' ', 0, start_nn)
        if index < 0:
            index = 0

        # if index + 10 < len(text_base):
        #     fragment = text_base[index:index+10]
        # else:
        #     fragment = text_base[index:]
        # print(f'index={index} text="...{fragment}..."')


        # Возьмём токен из текста результата для поиска в основном тексте
        tokens = text_nn.split()
        token_start_nn = None
        token_end_nn = None
        if len(tokens) > 0:
            token_start_nn = tokens[0]
            token_end_nn = tokens[-1]
        if not token_start_nn or not token_end_nn:
            # print('Tokens doesn\'t exist')
            return


        # Найдём подстроку с симптомом в основном тексте
        start_base = text_base.find(token_start_nn, index)
        if start_base < 0:
            # print(f'Token "{token_start_nn}" not found')
            return
        # else:
            # if start_base + 10 < len(text_base):
            #     fragment = text_base[start_base:start_base+10]
            # else:
            #     fragment = text_base[start_base:]
            # print(f'index={start_base} text="...{fragment}..."')
        while start_base > 0 and text_base[start_base - 1].isalpha():
            start_base -= 1


        # Найдём конец симптома в основном тексте
        index = start_base
        for token in tokens:
            index = text_base.find(token, index)
            if index == -1:
                # print(f'Next token "{token}" not found')
                return
        end_base = index + len(tokens[-1])

        text_symptom = text_base[start_base:end_base]
        # print(f'start={start_base} end={end_base} text="{text_symptom}"')

        return start_base, end_base, text_symptom
