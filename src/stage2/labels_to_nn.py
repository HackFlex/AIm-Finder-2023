import json

EMPTY_TOKEN = 0
START_TOKEN = 1
CONTINUE_TOKEN = 2


def debug(sd: dict, words):
    for key, value in sd.items():
        word = words[value]
        print(f"sd: {key} -> {word}")


class LabelToNN:
    def __init__(self) -> None:
        self.data = None
        self.result = {"tokens": [], "ner_tags": []}

    def load(self, filename) -> None:
        with open(filename) as f:
            self.data = json.load(f)

    def run(self) -> None:
        for item in self._get_next_item(self.data):
            # 1
            bounds = [bound for bound in self._get_next_bound(item)]
            bounds.sort()

            # 2
            text = self._get_text(item)

            words = []
            labels = []

            start_counter = 0

            while start_counter < len(text):
                end_counter = text.find(" ", start_counter)
                if end_counter == -1:
                    word = text[start_counter:]
                    end_counter = len(text)
                else:
                    word = text[start_counter:end_counter]

                if len(word) > 0:
                    self._add_word_and_label(
                        word, start_counter, end_counter, words, labels, bounds
                    )

                start_counter += end_counter - start_counter + 1

            self.result["tokens"].append(words)
            self.result["ner_tags"].append(labels)
        return self.result

    def _add_word_and_label(
        self,
        word: str,
        start_counter: int,
        end_counter: int,
        words: list,
        labels: list,
        bounds: list,
    ) -> None:
        if len(bounds) == 0:
            words.append(word)
            labels.append(EMPTY_TOKEN)
            return

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
            word1 = word[: bound_left - start_counter]
            if len(word1) > 0:
                words.append(word1)
            labels.append(EMPTY_TOKEN)

            word2 = word[bound_left - start_counter:]
            if len(word2) > 0:
                words.append(word2)
            labels.append(START_TOKEN)

        # 1
        elif start_counter < bound_left:
            words.append(word)
            labels.append(EMPTY_TOKEN)

        if bound_right < start_counter:
            bounds.pop(0)
            self._add_word_and_label(
                word, start_counter, end_counter, words, labels, bounds
            )

    def _get_next_item(self, data: list) -> dict:
        i = 0
        while i < len(data):
            yield data[i]
            i += 1

    def _get_next_bound(self, item: dict) -> tuple[int, int]:
        i = 0
        result = item["annotations"][0]["result"]
        while i < len(result):
            value = result[i]["value"]
            yield value["start"], value["end"]
            i += 1

    def _get_text(self, item: dict) -> str:
        return item["data"]["text"]


if __name__ == "__main__":
    filename = "dataset/Пример_разметки_из_label_studio.json"

    translater = LabelToNN()
    translater.load(filename)
    result = translater.run()
    print(result["tokens"])
    print(result["ner_tags"])
