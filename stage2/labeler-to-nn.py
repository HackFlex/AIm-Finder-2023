import json

EMPTY_TOKEN = 0
START_TOKEN = 1
CONTINUE_TOKEN = 2

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

            words = []
            labels = []

            start_counter = 0

            while start_counter < len(text):
                end_counter = text.find(' ', start_counter)
                if end_counter == -1:
                    word = text[start_counter:]
                    end_counter = len(text)
                else:
                    word = text[start_counter:end_counter]

                if len(word) > 0:

                    if len(bounds) > 0:
                        bound_left = bounds[0][0]
                        bound_right = bounds[0][1]

                        # 3
                        if bound_left <= start_counter < bound_right:
                                        
                            words.append(word)
                            
                            if bound_left == start_counter:
                                labels.append(START_TOKEN)
                            else:
                                labels.append(CONTINUE_TOKEN)

                        # ex
                        elif start_counter < bound_left < end_counter:

                            word1 = text[start_counter:bound_left]
                            if len(word1) > 0:
                                words.append(word1)
                            labels.append(EMPTY_TOKEN)

                            word2 = text[bound_left:end_counter]
                            if len(word2) > 0:
                                words.append(word2)
                            labels.append(START_TOKEN)

                        # 1
                        elif start_counter < bound_left:

                            words.append(word)
                            labels.append(EMPTY_TOKEN)

                        if bound_right < start_counter:
                            bounds.pop(0)

                    else:
                        words.append(word)
                        labels.append(EMPTY_TOKEN)

                start_counter += end_counter - start_counter + 1
            
            for i in range(len(words)):
                print(f'{i:3}: {words[i]} -> {labels[i]}')

            print(len(text.split()))

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
    
