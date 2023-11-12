import shlex
import subprocess
from enum import Enum

class BoundStatus(Enum):
    UNIQUE = 0
    REPEAT = 1
    INTERSECT = 2

ALLOWED_SPECIAL_CHAR = {'/', ','}

IS_PRINT_DEBUG = False

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
        bounds = []
        text_base = srcSection['name']
        
        if IS_PRINT_DEBUG:
            tmp_index = 0
            tmp_step = 50
            while tmp_index < len(text_base):
                print(f'{tmp_index:3} | {text_base[tmp_index:tmp_index+tmp_step]}')
                tmp_index += tmp_step

        for symptom in outSection['symptoms']:

            start_nn, end_nn = [int(item) for item in symptom]
            text_nn = outSection['text'][start_nn:end_nn]

            result = self.__get_real_bounds_and_text(
                text_base, text_nn, start_nn, end_nn)
            if result is None:
                continue
            start_base, end_base, text_symptom = result

            current_bound = (start_base, end_base)
            bound_status = self.__get_bound_status(bounds, current_bound)
            if bound_status[0] != BoundStatus.UNIQUE:
                if bound_status[0] == BoundStatus.REPEAT:
                    if IS_PRINT_DEBUG:
                        print(f'REPEAT: "{text_symptom}"')
                    pass
                elif bound_status[0] == BoundStatus.INTERSECT:
                    index = bound_status[1][0]
                    new_bound = bound_status[1][1]
                    bounds[index] = new_bound
                    arrSymptoms[index]['start'] = new_bound[0]
                    arrSymptoms[index]['end'] = new_bound[1]
                    arrSymptoms[index]['name'] = text_base[new_bound[0]:new_bound[1]]
                    if IS_PRINT_DEBUG:
                        print(f'INTERSECT: start={new_bound[0]} end={new_bound[1]} text="{text_base[new_bound[0]:new_bound[1]]}"')
                continue
            bounds.append(current_bound)

            symptomJson = self._getSymptomJson(
                srcSection['xPath'],
                start_base,
                end_base,
                text_symptom)
            arrSymptoms.append(symptomJson)
        return arrSymptoms
    
    def __get_bound_status(self, bounds: list[tuple[int, int]],
                           current_bound: tuple[int, int]
                           ) -> tuple[BoundStatus, tuple[int, tuple[int, int]] or None]:
        i = 0
        for bound in bounds:
            if current_bound == bound:
                return BoundStatus.REPEAT,
            if current_bound[0] < bound[1] < current_bound[1]:
                return BoundStatus.INTERSECT, (i, (bound[0], current_bound[1]))
            if current_bound[0] < bound[0] < current_bound[1]:
                return BoundStatus.INTERSECT, (i, (current_bound[0], bound[1]))
            i += 1
        return BoundStatus.UNIQUE,

    def __is_allowed_char(self, c: str) -> bool:
        return c in ALLOWED_SPECIAL_CHAR or c.isalnum()
    
    def __is_correct_text(self, text: str) -> bool:
        tmp_text = text.replace(' ', '')
        for c in ALLOWED_SPECIAL_CHAR:
            tmp_text = tmp_text.replace(c, '')
        # print(tmp_text)
        return len(tmp_text) > 0 and tmp_text.isalnum()
    
    def __get_real_bounds_and_text(self, text_base: str, text_nn: str,
                                   start_nn: int, end_nn: int):
        if IS_PRINT_DEBUG:
            print(f'start={start_nn} end={end_nn} text="{text_nn}"', end=' | ')

        # Надо понять, как отсечь варианты, в которых нет цифр и букв
        if not self.__is_correct_text(text_nn):
            if IS_PRINT_DEBUG:
                print('This is the wrong text')
            return
        
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
        while start_base > 0 and self.__is_allowed_char(text_base[start_base - 1]):
            start_base -= 1

        # Найдём конец симптома в основном тексте
        index = start_base
        for token in tokens:
            index = text_base.find(token, index)
            if index == -1:
                # print(f'Next token "{token}" not found')
                return
        end_base = index + len(tokens[-1])
        while end_base < len(text_base) and self.__is_allowed_char(text_base[end_base]):
            end_base += 1

        text_symptom = text_base[start_base:end_base]
        if IS_PRINT_DEBUG:
            print(f'start={start_base} end={end_base} text="{text_symptom}"')

        return start_base, end_base, text_symptom
