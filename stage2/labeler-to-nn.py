import json


def debug(sd: dict, words):
    for key, value in sd.items():
        word = words[value]
        print(f'sd: {key} -> {word}')


class LabelToNN:
    def __init__(self) -> None:
        self.data = None
        self.result = {
            'words': [],
            'labels': []
        }


    def load(self, filename) -> None:
        with open(filename) as f:
            self.data = json.load(f)


    def run(self) -> None:

        for item in self.__get_next_item(self.data):

            # 1
            bounds = [bound for bound in self.__get_next_bound(item)]
            bounds.sort()

            # 2
            text = self.__get_text(item)
            # start_word, end_word = self.__create_bound_dict(text)

            start_word = {}
            end_word = {}
            words = []
            labels = []

            start_counter = 0
            index = 0
            flag = 0
            while start_counter < len(text):
                end_counter = text.find(' ', start_counter)
                if end_counter == -1:
                    word = text[start_counter:]
                    end_counter = len(text)
                else:
                    word = text[start_counter:end_counter]

                if len(bounds) > 0:
                    # 3
                    if bounds[0][0] <= start_counter < bounds[0][1]:
                                    
                        if len(word) > 0:
                            words.append(word)
                            start_word[start_counter] = words[-1]
                            end_word[words[-1]] = end_counter
                            index += 1
                        
                        if bounds[0][0] == start_counter:
                            labels.append(1)
                        else:
                            labels.append(2)

                    # ex
                    elif start_counter < bounds[0][0] < end_counter:

                        word1 = text[start_counter:bounds[0][0]]
                        if len(word1) > 0:
                            words.append(word1)
                            start_word[start_counter] = words[-1]
                            end_word[words[-1]] = end_counter
                            index += 1
                        labels.append(0)

                        word2 = text[bounds[0][0]:end_counter]
                        if len(word2) > 0:
                            words.append(word2)
                            start_word[start_counter] = words[-1]
                            end_word[words[-1]] = end_counter
                            index += 1
                        labels.append(1)

                    # 1
                    elif start_counter < bounds[0][0]:

                        if len(word) > 0:
                            words.append(word)
                            start_word[start_counter] = words[-1]
                            end_word[words[-1]] = end_counter
                            index += 1
                        labels.append(0)

                    # 4
                    elif bounds[0][1] < start_counter:

                        if len(word) > 0:
                            words.append(word)
                            start_word[start_counter] = words[-1]
                            end_word[words[-1]] = end_counter
                            index += 1
                        labels.append(0)



                start_counter += end_counter - start_counter + 1
            

            for bound_start, bound_end in self.__get_next_bound(item):
                count = 0
                index = start_word.get(bound_start, -1)
                if index == -1:
                    print(f'ERROR: {bound_start}')
                    # print(start_word)
                    debug(start_word, words)

                    exit(1)
                labels[index] = 1
                count += 1
                while end_word[index] <= bound_end:
                    index += 1
                    labels[index] = 2
                    count += 1
                print(f'{bound_start} -> {bound_end}: {count}')

            break


    def __create_bound_dict(self, text) -> tuple[dict, dict]:
        start_word = {}
        end_word = {}

        start_counter = 0
        index = 0
        while start_counter < len(text):
            end_counter = text.find(' ', start_counter)
            if end_counter == -1:
                word = text[start_counter:]
                end_counter = len(text)
            else:
                word = text[start_counter:end_counter]
            
            # print(f'"{word}" [{start_counter}, {end_counter - 1}]')
            start_word[start_counter] = index
            # end_word[end_counter] = index
            end_word[index] = end_counter

            start_counter += end_counter - start_counter + 1
            index += 1

        return start_word, end_word


    def __get_next_item(self, data: list) -> dict:
        i = 0
        while i < len(data):
            yield data[i]
            i += 1

    def __get_next_bound(self, item: dict) -> tuple[int, int]:
        i = 0
        result = item['annotations'][0]['result']
        while i < len(result):
            value = result[i]['value']
            yield value['start'], value['end']
            i += 1


    def __get_text(self, item: dict) -> str:
        return item['data']['text']


if __name__ == '__main__':
    filename = '../dataset/Пример_разметки.json'
    
    trans = LabelToNN()
    trans.load(filename)
    trans.run()
    
